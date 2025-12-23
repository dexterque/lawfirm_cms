import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawfirm_cms.settings.production')
django.setup()

from wagtail.models import Page

print("=== All Pages ===")
for p in Page.objects.all():
    print(f"ID:{p.id} Slug:{p.slug} Title:{p.title} Live:{p.live}")
