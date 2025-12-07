#!/usr/bin/env python3
import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawfirm_cms.settings.dev')
import django
django.setup()
from team.models import TeamIndexPage, TeamMemberPage

# find TeamIndexPage by slug
try:
    idx = TeamIndexPage.objects.get(slug='zhuanyetuandui')
except TeamIndexPage.DoesNotExist:
    print('TeamIndexPage with slug zhuanyetuandui not found')
    idx = None

if idx:
    # create a dummy request-like object with path '/lvshizhurenzhuli/'
    class Req:
        path = '/lvshizhurenzhuli/'
    ctx = idx.get_context(Req())
    members = ctx.get('members')
    print('members total:', members.count() if hasattr(members, 'count') else len(members))
    print('team_host:', len(ctx.get('team_host', [])))
    print('team_chief_assistant:', len(ctx.get('team_chief_assistant', [])))
    print('team_business_assistant:', len(ctx.get('team_business_assistant', [])))
    print('team_others:', len(ctx.get('team_others', [])))
    print('\nList titles per category:')
    for k in ['team_host','team_chief_assistant','team_business_assistant']:
        print(k, [p.title for p in ctx.get(k, [])])

    # Also print raw members titles
    print('\nAll members titles:')
    print([m.title for m in members])
