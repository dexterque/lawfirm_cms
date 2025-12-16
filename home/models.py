from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel

# ... (rest of imports are same, skipping lines)

# ... (existing classes: HomePageBanner, HomePageServiceItem, HomePageTeamMember, HomePage)

    content_panels = Page.content_panels + [
        InlinePanel('banners', label="轮播图"),
        InlinePanel('service_items', label="业务领域图标"),
        MultiFieldPanel([
            FieldPanel('main_lawyer_name'),
            FieldPanel('main_lawyer_position'),
            FieldPanel('main_lawyer_photo'),
            FieldPanel('main_lawyer_link'),
        ], heading="主律师信息"),
        InlinePanel('team_members', label="首页团队成员"),
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
