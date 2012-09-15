import datetime
import itertools
import re

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.views.decorators.vary import vary_on_headers

from parliament.activity.models import Activity
from parliament.activity import utils as activity
from parliament.core.models import Politician, ElectedMember
from parliament.core.utils import feed_wrapper
from parliament.hansards.models import Statement, Document
from parliament.utils.views import JSONView

def current_mps(request):
    t = loader.get_template('politicians/electedmember_list.html')
    c = RequestContext(request, {
        'object_list': ElectedMember.objects.current().order_by(
            'riding__province', 'politician__name_family').select_related('politician', 'riding', 'party'),
        'title': 'Current Members of Parliament'
    })
    return HttpResponse(t.render(c))
        
def former_mps(request):
    former_members = ElectedMember.objects.exclude(end_date__isnull=True)\
        .order_by('riding__province', 'politician__name_family', '-start_date')\
        .select_related('politician', 'riding', 'party')
    seen = set()
    object_list = []
    for member in former_members:
        if member.politician_id not in seen:
            object_list.append(member)
            seen.add(member.politician_id)
    
    c = RequestContext(request, {
        'object_list': object_list,
        'title': 'Former MPs (since 1994)'
    })
    t = loader.get_template("politicians/former_electedmember_list.html")
    return HttpResponse(t.render(c))

@vary_on_headers('X-Requested-With')
def politician(request, pol_id=None, pol_slug=None):
    if pol_slug:
        pol = get_object_or_404(Politician, slug=pol_slug)
    else:
        pol = get_object_or_404(Politician, pk=pol_id)
        if pol.slug:
            return HttpResponsePermanentRedirect(pol.get_absolute_url())
    
    show_statements = bool('page' in request.GET or 
        (pol.latest_member and not pol.latest_member.current))
    
    if show_statements:
        STATEMENTS_PER_PAGE = 10
        statements = pol.statement_set.filter(
            procedural=False, document__document_type=Document.DEBATE).order_by('-time', '-sequence')
        paginator = Paginator(statements, STATEMENTS_PER_PAGE)
        try:
            pagenum = int(request.GET.get('page', '1'))
        except ValueError:
            pagenum = 1
        try:
            statement_page = paginator.page(pagenum)
        except (EmptyPage, InvalidPage):
            statement_page = paginator.page(paginator.num_pages)
    else:
        statement_page = None
        
    c = RequestContext(request, {
        'pol': pol,
        'member': pol.latest_member,
        'candidacies': pol.candidacy_set.all().order_by('-election__date'),
        'electedmembers': pol.electedmember_set.all().order_by('-start_date'),
        'page': statement_page,
        'statements_politician_view': True,
        'show_statements': show_statements,
        'activities': activity.iter_recent(Activity.public.filter(politician=pol)),
        'search_placeholder': u"Search %s in Parliament" % pol.name
    })
    if request.is_ajax():
        t = loader.get_template("hansards/statement_page_politician_view.inc")
    else:
        t = loader.get_template("politicians/politician.html")
    return HttpResponse(t.render(c))

def contact(request, pol_id=None, pol_slug=None):
    if pol_slug:
        pol = get_object_or_404(Politician, slug=pol_slug)
    else:
        pol = get_object_or_404(Politician, pk=pol_id)

    if not pol.current_member:
        raise Http404

    c = RequestContext(request, {
        'pol': pol,
        'info': pol.info(),
        'title': u'Contact %s' % pol.name
    })
    t = loader.get_template("politicians/contact.html")
    return HttpResponse(t.render(c))
    
def hide_activity(request):
    if not request.user.is_authenticated() and request.user.is_staff:
        raise PermissionDenied
        
    activity = Activity.objects.get(pk=request.POST['activity_id'])
    activity.active = False
    activity.save()
    return HttpResponse('OK')

class PoliticianAutocompleteView(JSONView):

    def get(self, request):

        q = request.GET.get('q', '').lower()

        if not hasattr(self, 'politician_list'):
            self.politician_list = list(Politician.objects.elected().values(
                'name', 'name_family', 'slug', 'id').order_by('name_family'))

        results = (
            {'value': p['slug'] if p['slug'] else unicode(p['id']), 'label': p['name']}
            for p in self.politician_list
            if p['name'].lower().startswith(q) or p['name_family'].lower().startswith(q)
        )
        return list(itertools.islice(results, 15))
politician_autocomplete = PoliticianAutocompleteView.as_view()

class PoliticianStatementFeed(Feed):
    
    def get_object(self, request, pol_id):
        self.language = request.GET.get('language', settings.LANGUAGE_CODE)
        return get_object_or_404(Politician, pk=pol_id)
    
    def title(self, pol):
        return "%s in the House of Commons" % pol.name
        
    def link(self, pol):
        return "http://openparliament.ca" + pol.get_absolute_url()
        
    def description(self, pol):
        return "Statements by %s in the House of Commons, from openparliament.ca." % pol.name
        
    def items(self, pol):
        return Statement.objects.filter(
            member__politician=pol, document__document_type=Document.DEBATE).order_by('-time')[:12]
        
    def item_title(self, statement):
        return statement.topic
        
    def item_link(self, statement):
        return statement.get_absolute_url()
        
    def item_description(self, statement):
        return statement.text_html(language=self.language)
        
    def item_pubdate(self, statement):
        return statement.time

politician_statement_feed = feed_wrapper(PoliticianStatementFeed)
        
r_title = re.compile(r'<span class="tag.+?>(.+?)</span>')
r_link = re.compile(r'<a [^>]*?href="(.+?)"')
r_excerpt = re.compile(r'<span class="excerpt">')

class PoliticianActivityFeed(Feed):

    def get_object(self, request, pol_id):
        return get_object_or_404(Politician, pk=pol_id)

    def title(self, pol):
        return pol.name

    def link(self, pol):
        return "http://openparliament.ca" + pol.get_absolute_url()

    def description(self, pol):
        return "Recent news about %s, from openparliament.ca." % pol.name

    def items(self, pol):
        return activity.iter_recent(Activity.objects.filter(politician=pol))

    def item_title(self, activity):
        # FIXME wrap in try
        return r_title.search(activity.payload).group(1)

    def item_link(self, activity):
        match = r_link.search(activity.payload)
        if match:
            return match.group(1)
        else:
            # FIXME include links in activity model?
            return ''
            
    def item_guid(self, activity):
        return activity.guid
    
    def item_description(self, activity):
        payload = r_excerpt.sub('<br><span style="display: block; border-left: 1px dotted #AAAAAA; margin-left: 2em; padding-left: 1em; font-style: italic; margin-top: 5px;">', activity.payload_wrapped())
        payload = r_title.sub('', payload)
        return payload
        
    def item_pubdate(self, activity):
        return datetime.datetime(activity.date.year, activity.date.month, activity.date.day)