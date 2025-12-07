#!/usr/bin/env python3
import os,sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
if proj_root not in sys.path: sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','lawfirm_cms.settings.dev')
import django
django.setup()
from team.models import TeamIndexPage, TeamMemberPage
from wagtail.models import Page

pages = TeamIndexPage.objects.all()
print('Found', pages.count(), 'TeamIndexPage instances')
for p in pages:
    # count direct child TeamMemberPage under this page
    child_count = TeamMemberPage.objects.child_of(p).live().count()
    print('slug:', p.slug, 'title:', p.title, 'children:', child_count, 'url:', p.get_url_parts())

# also print root pages that match path
root = Page.get_first_root_node()
print('root slug', root.slug)
