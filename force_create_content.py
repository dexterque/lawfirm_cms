import sys
# Monkeypatch BEFORE importing models or running signals
try:
    import modelsearch.signal_handlers
    print("Monkeypatching modelsearch.signal_handlers.post_save_signal_handler")
    modelsearch.signal_handlers.post_save_signal_handler = lambda *args, **kwargs: None
    modelsearch.signal_handlers.post_delete_signal_handler = lambda *args, **kwargs: None
except ImportError:
    pass

from home.models import HomePage
from article.models import ArticleIndexPage
from team.models import TeamIndexPage
from service.models import ServiceIndexPage
from about.models import AboutPage
from wagtail.models import Page

def run():
    try:
        homepage = Page.objects.get(slug='home').specific
    except Page.DoesNotExist:
        print("Home page not found")
        return

    # Force fix numchild
    real_children = Page.objects.child_of(homepage).count()
    print(f"Real children: {real_children}, Stored numchild: {homepage.numchild}")
    
    if homepage.numchild != real_children:
        print(f"Fixing numchild to {real_children}")
        Page.objects.filter(pk=homepage.pk).update(numchild=real_children)
        homepage.refresh_from_db()
    
    # Define pages
    pages_data = [
        {'model': ArticleIndexPage, 'title': '经典案例', 'slug': 'jingdiananli', 'intro': '这里是经典案例列表...'},
        {'model': ServiceIndexPage, 'title': '业务领域', 'slug': 'yewulingyu', 'intro': '我们提供的法律服务领域...'},
        {'model': TeamIndexPage, 'title': '专业团队', 'slug': 'zhuanyetuandui', 'intro': '我们的专业律师团队...'},
        {'model': ArticleIndexPage, 'title': '新闻动态', 'slug': 'xinwendongtai', 'intro': '最新的律所新闻和动态...'},
        {'model': ArticleIndexPage, 'title': '知识课堂', 'slug': 'zhishiketang', 'intro': '法律知识科普...'},
        {'model': AboutPage, 'title': '关于我们', 'slug': 'guanyuwomen', 'body': '<p>北京翰汇律师事务所...</p>'},
    ]

    for data in pages_data:
        model = data['model']
        slug = data['slug']
        title = data['title']
        
        if model.objects.child_of(homepage).filter(slug=slug).exists():
            print(f"{title} exists")
            continue
            
        print(f"Creating {title}...")
        if model == AboutPage:
            page = model(title=title, slug=slug, body=data.get('body', ''))
        else:
            page = model(title=title, slug=slug, intro=data.get('intro', ''))
            
        homepage.add_child(instance=page)
        page.save_revision().publish()
        print(f"Created {title}")

if __name__ == "__main__":
    run()
run()
