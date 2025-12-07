#!/usr/bin/env python3
import os, sys
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawfirm_cms.settings.dev')
import django
django.setup()
from django.test import Client

def check(path):
    c = Client()
    r = c.get(path)
    s = r.content.decode('utf-8', 'replace')
    print('GET', path, 'STATUS', r.status_code)
    count = s.count('class="team-member"')
    print('team-member count:', count)
    start = s.find('<div class="team-content')
    if start != -1:
        print(s[start:start+800])
    else:
        print('team-content not found')

if __name__ == '__main__':
    check('/lvshizhurenzhuli/')
    print('\n---\n')
    check('/zhubanlvshi/')
    print('\n---\n')
    check('/lvshiyewuzhuli/')
