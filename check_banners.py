import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawfirm_cms.settings.production')
django.setup()

from home.models import HomePage, HomePageBanner

# 获取首页
home = HomePage.objects.first()
if home:
    print(f"HomePage ID: {home.id}")
    banners = home.banners.all()
    print(f"Banners count: {banners.count()}")
    for b in banners:
        img_exists = "YES" if b.image and os.path.exists(b.image.file.path) else "NO"
        print(f"  Banner: {b.title} | Image: {b.image} | File exists: {img_exists}")
else:
    print("No HomePage found")
