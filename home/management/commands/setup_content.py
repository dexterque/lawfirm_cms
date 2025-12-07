from django.core.management.base import BaseCommand
from wagtail.models import Page
from home.models import HomePage
from article.models import ArticleIndexPage
from team.models import TeamIndexPage
from service.models import ServiceIndexPage
from about.models import AboutPage
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Creates initial content manually to bypass treebeard issues'

    def handle(self, *args, **options):
        try:
            homepage = Page.objects.get(slug='home').specific
        except Page.DoesNotExist:
            self.stdout.write(self.style.ERROR("HomePage not found"))
            return

        base_path = homepage.path
        if not base_path:
            self.stdout.write(self.style.ERROR("HomePage has no path"))
            return

        # alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # steplen = 4
        # We manually calculate standard paths since we know the alphabet
        
        # 000100010001, 000100010002, etc.
        def get_next_path(base, index):
            # Simple hex-like increment for the last segment
            # Assuming standard numeric-first alphabet
            # 0001, 0002, ...
            # index is 1-based
            suffix = f"{index:04d}"
            return base + suffix

        pages_data = [
            {'model': ArticleIndexPage, 'title': '经典案例', 'slug': 'jingdiananli', 'intro': '这里是经典案例列表...'},
            {'model': ServiceIndexPage, 'title': '业务领域', 'slug': 'yewulingyu', 'intro': '我们提供的法律服务领域...'},
            {'model': TeamIndexPage, 'title': '专业团队', 'slug': 'zhuanyetuandui', 'intro': '我们的专业律师团队...'},
            {'model': ArticleIndexPage, 'title': '新闻动态', 'slug': 'xinwendongtai', 'intro': '最新的律所新闻和动态...'},
            {'model': ArticleIndexPage, 'title': '知识课堂', 'slug': 'zhishiketang', 'intro': '法律知识科普...'},
            {'model': AboutPage, 'title': '关于我们', 'slug': 'guanyuwomen', 'body': '<p>北京翰汇律师事务所...</p>'},
        ]

        current_child_count = homepage.get_children().count()
        start_index = current_child_count + 1

        for i, data in enumerate(pages_data):
            idx = start_index + i
            model = data['model']
            slug = data['slug']
            title = data['title']
            
            if model.objects.filter(slug=slug).exists():
                self.stdout.write(f"{title} already exists")
                continue

            path = get_next_path(base_path, idx)
            depth = homepage.depth + 1
            
            self.stdout.write(f"Creating {title} at {path}")
            
            kwargs = {
                'title': title,
                'slug': slug,
                'path': path,
                'depth': depth,
                'numchild': 0,
                'live': True,
                'locale': homepage.locale,
            }

            if model == AboutPage:
                kwargs['body'] = data.get('body', '')
            elif model in [ArticleIndexPage, TeamIndexPage, ServiceIndexPage]:
                kwargs['intro'] = data.get('intro', '')

            page = model(**kwargs)
            page.save()
            
            # Manually update parent numchild
            homepage.numchild += 1
            homepage.save()

            # Create an initial revision
            page.save_revision().publish()

        self.stdout.write(self.style.SUCCESS("Manual creation complete"))
