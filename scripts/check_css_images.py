#!/usr/bin/env python3
import os, re, sys
# Ensure project root is on sys.path so the inner `lawfirm_cms` package is importable
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawfirm_cms.settings.dev')
import django
django.setup()
from django.test import Client
from django.conf import settings

def main():
    c = Client()
    r = c.get('/')
    s = r.content.decode('utf-8', 'replace')
    links = re.findall(r"<link[^>]+href=[\'\"]([^\'\"]+\.css)[\'\"]", s)
    print('STATUS', r.status_code)
    tokens = ['news.png', 'about_us.png', 'bg-Professional_team.png']
    for l in links:
        print('CSS:', l)
        if l.startswith('/'):
            rel = l.lstrip('/')
            candidates = []
            if getattr(settings, 'STATIC_ROOT', None):
                candidates.append(os.path.join(settings.STATIC_ROOT, rel.replace('/', os.sep)))
            for d in getattr(settings, 'STATICFILES_DIRS', []):
                candidates.append(os.path.join(d, rel))
            try:
                candidates.append(os.path.join(settings.BASE_DIR, rel))
            except Exception:
                pass
            found = False
            for cpath in candidates:
                if os.path.exists(cpath):
                    print('  Found file:', cpath)
                    with open(cpath, 'r', encoding='utf-8', errors='replace') as fh:
                        data = fh.read()
                    for t in tokens:
                        if t in data:
                            print('   Contains', t)
                    found = True
                    break
            if not found:
                print('  File not found on disk; skip')
        else:
            print('  External CSS; skip')

if __name__ == '__main__':
    main()
