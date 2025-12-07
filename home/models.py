from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.models import Image
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable


class HomePageBanner(Orderable):
    """轮播图"""
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='banners')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)

    panels = [
        FieldPanel('image'),
        FieldPanel('title'),
        FieldPanel('subtitle'),
        FieldPanel('link'),
    ]


class HomePageServiceItem(Orderable):
    """业务领域项目"""
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='service_items')
    title = models.CharField(max_length=100)
    icon_red = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    icon_white = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    link = models.URLField(blank=True, default='/yewulingyu/')

    panels = [
        FieldPanel('title'),
        FieldPanel('icon_red'),
        FieldPanel('icon_white'),
        FieldPanel('link'),
    ]


class HomePageTeamMember(Orderable):
    """首页团队成员"""
    page = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=200, blank=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    link = models.URLField(blank=True, default='/zhuanyetuandui/')

    panels = [
        FieldPanel('name'),
        FieldPanel('position'),
        FieldPanel('photo'),
        FieldPanel('link'),
    ]


class HomePage(Page):
    # 关于我们简介
    about_intro = RichTextField(blank=True, verbose_name="关于我们简介")
    
    # 主律师信息
    main_lawyer_name = models.CharField(max_length=100, blank=True, default='吴少博')
    main_lawyer_position = models.CharField(max_length=200, blank=True, default='北京吴少博律师事务所创始人、主任')
    main_lawyer_photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    main_lawyer_link = models.URLField(blank=True, default='/zhuanyetuandui/')

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('main_lawyer_name'),
            FieldPanel('main_lawyer_position'),
            FieldPanel('main_lawyer_photo'),
            FieldPanel('main_lawyer_link'),
        ], heading="主律师信息"),
        FieldPanel('about_intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        
        from article.models import ArticlePage, ArticleIndexPage
        from team.models import TeamMemberPage, TeamIndexPage
        
        # 新闻动态
        news_index = ArticleIndexPage.objects.filter(slug='xinwendongtai').first()
        if news_index:
            context['news_list'] = ArticlePage.objects.child_of(news_index).live().order_by('-date')[:3]
        
        # 经典案例
        cases_index = ArticleIndexPage.objects.filter(slug='jingdiananli').first()
        if cases_index:
            context['cases_list'] = ArticlePage.objects.child_of(cases_index).live().order_by('-date')[:5]
            
        # 知识课堂
        knowledge_index = ArticleIndexPage.objects.filter(slug='zhishiketang').first()
        if knowledge_index:
            context['knowledge_list'] = ArticlePage.objects.child_of(knowledge_index).live().order_by('-date')[:6]
        
        # 团队成员（从专业团队页面获取）
        team_index = TeamIndexPage.objects.filter(slug='zhuanyetuandui').first()
        if team_index:
            context['team_list'] = TeamMemberPage.objects.child_of(team_index).live()[:6]
            
        return context
