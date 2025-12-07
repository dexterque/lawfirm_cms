#!/usr/bin/env python3
import os,sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
if proj_root not in sys.path: sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','lawfirm_cms.settings.dev')
import django
django.setup()
from django.test import Client
c=Client()
r=c.get('/lvshizhurenzhuli/')
s=r.content.decode('utf-8','replace')
print('len',len(s))
print('team-member occurrences', s.count('team-member'))
print('wu present', '吴少博' in s)
print('li present', '李静' in s)
print('wu idx', s.find('吴少博'))
print('li idx', s.find('李静'))
start = s.find('<div class="team-filters"')
if start!=-1:
    print(s[start:start+4000])
else:
    print('team-filters not found')
