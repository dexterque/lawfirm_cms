import sys
from django.conf import settings

# Monkeypatch django_tasks to avoid the TypeError
try:
    import django_tasks.backends.immediate
    print("Monkeypatching django_tasks.backends.immediate.ImmediateBackend.enqueue")
    
    def dummy_enqueue(self, task, args, kwargs):
        print(f"Skipping task enqueue: {task}")
        return None

    django_tasks.backends.immediate.ImmediateBackend.enqueue = dummy_enqueue
except ImportError:
    print("django_tasks not found, skipping patch")
except Exception as e:
    print(f"Failed to patch django_tasks: {e}")

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
        # If home doesn't exist by slug, try getting the one at depth 2
        homepage_q = Page.objects.filter(depth=2).first()
        if homepage_q:
            homepage = homepage_q.specific
            print(f"Found homepage by depth: {homepage.title}")
        else:
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
        {'model': ArticleIndexPage, 'title': '获赠锦旗', 'slug': 'huozengjinqi', 'intro': '获赠锦旗...'},
        
        {'model': ServiceIndexPage, 'title': '业务领域', 'slug': 'yewulingyu', 'intro': '我们提供的法律服务领域...'},
        
        {'model': TeamIndexPage, 'title': '专业团队', 'slug': 'zhuanyetuandui', 'intro': '我们的专业律师团队...'},
        {'model': TeamIndexPage, 'title': '主办律师', 'slug': 'zhubanlvshi', 'intro': '主办律师团队...'},
        {'model': TeamIndexPage, 'title': '律师主任助理', 'slug': 'lvshizhurenzhuli', 'intro': '律师主任助理团队...'},
        {'model': TeamIndexPage, 'title': '律师业务助理', 'slug': 'lvshiyewuzhuli', 'intro': '律师业务助理团队...'},
        
        {'model': ArticleIndexPage, 'title': '新闻动态', 'slug': 'xinwendongtai', 'intro': '最新的律所新闻和动态...'},
        
        {'model': ArticleIndexPage, 'title': '知识课堂', 'slug': 'zhishiketang', 'intro': '法律知识科普...'},
        {'model': ArticleIndexPage, 'title': '普法视频', 'slug': 'pufashipin', 'intro': '普法视频...'},
        {'model': ArticleIndexPage, 'title': '维权书籍', 'slug': 'weiquanshuji', 'intro': '维权书籍...'},
        {'model': ArticleIndexPage, 'title': '热点普法', 'slug': 'redianpufa', 'intro': '热点普法...'},
        
        {'model': AboutPage, 'title': '关于我们', 'slug': 'guanyuwomen', 'body': '<p>北京翰汇律师事务所...</p>'},
        {'model': AboutPage, 'title': '联系我们', 'slug': 'lianxiwomen', 'body': '<p>联系方式...</p>'},
        {'model': AboutPage, 'title': '加入律所', 'slug': 'jiarulvsuo', 'body': '<p>加入我们...</p>'},
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
