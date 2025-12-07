from django.core.files import File
from home.models import HomePage
from article.models import ArticleIndexPage
from team.models import TeamIndexPage
from service.models import ServiceIndexPage
from about.models import AboutPage
from wagtail.models import Page, Site

def run():
    # Get the homepage
    try:
        homepage = Page.objects.get(slug='home').specific
    except Page.DoesNotExist:
        print("HomePage not found. Please create one first.")
        return
    
    print(f"Found homepage: {homepage}, ID: {homepage.id}, Path: {homepage.path}, Depth: {homepage.depth}")

    # Define the pages to create
    pages_data = [
        {
            'model': ArticleIndexPage,
            'title': '经典案例',
            'slug': 'jingdiananli',
            'intro': '这里是经典案例列表...'
        },
        {
            'model': ServiceIndexPage,
            'title': '业务领域',
            'slug': 'yewulingyu',
            'intro': '我们提供的法律服务领域...'
        },
        {
            'model': TeamIndexPage,
            'title': '专业团队',
            'slug': 'zhuanyetuandui',
            'intro': '我们的专业律师团队...'
        },
        {
            'model': ArticleIndexPage,
            'title': '新闻动态',
            'slug': 'xinwendongtai',
            'intro': '最新的律所新闻和动态...'
        },
        {
            'model': ArticleIndexPage,
            'title': '知识课堂',
            'slug': 'zhishiketang',
            'intro': '法律知识科普...'
        },
        {
            'model': AboutPage,
            'title': '关于我们',
            'slug': 'guanyuwomen',
            'body': '<p>北京翰汇律师事务所...</p>'
        }
    ]

    for data in pages_data:
        model = data['model']
        slug = data['slug']
        title = data['title']
        
        # Check if page exists
        if not model.objects.filter(slug=slug).exists():
            print(f"Creating {title} ({slug})...")
            if model == AboutPage:
                page = model(title=title, slug=slug, body=data.get('body', ''))
            elif model == ArticleIndexPage or model == TeamIndexPage or model == ServiceIndexPage:
                page = model(title=title, slug=slug, intro=data.get('intro', ''))
            else:
                page = model(title=title, slug=slug)
            
            homepage.add_child(instance=page)
            page.save_revision().publish()
        else:
            print(f"{title} ({slug}) already exists.")

    print("Initial content creation complete.")

import traceback

try:
    run()
except Exception:
    import traceback
    traceback.print_exc()

