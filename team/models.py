from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

class TeamIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    subpage_types = ['team.TeamMemberPage']
    
    def get_context(self, request):
        context = super().get_context(request)
        # 获取具体的 TeamMemberPage 实例
        members = TeamMemberPage.objects.child_of(self).live().order_by('first_published_at')
        # 如果当前索引页没有子成员（例如这是按角色创建的空索引页），
        # 回退到主团队索引 `zhuanyetuandui` 的子成员以便复用同一成员集合。
        if not members.exists():
            try:
                fallback = TeamIndexPage.objects.get(slug='zhuanyetuandui')
                if fallback and fallback.id != self.id:
                    members = TeamMemberPage.objects.child_of(fallback).live().order_by('first_published_at')
            except TeamIndexPage.DoesNotExist:
                pass
        context['members'] = members
        context['members_with_photo'] = members.exclude(photo__isnull=True)
        # 分类：只保留 主办律师 和 律师业务助理
        categories = {
            '主办律师': [],
            '律师业务助理': [],
        }
        others = []
        for m in members:
            # 优先使用标准化的 `role` 字段进行分类
            if getattr(m, 'role', None):
                if m.role == 'host':
                    categories['主办律师'].append(m)
                    continue
                if m.role == 'business_assistant':
                    categories['律师业务助理'].append(m)
                    continue

            # 否则回退到自由文本 `position` 的模糊匹配（兼容历史数据）
            pos = (m.position or '').strip()
            if not pos:
                others.append(m)
                continue
            lowered = pos.lower()
            if '主办' in lowered or '主办律师' in lowered:
                categories['主办律师'].append(m)
            elif '业务助理' in lowered or '助理' in lowered:
                categories['律师业务助理'].append(m)
            else:
                others.append(m)

        context['team_categories'] = categories
        context['team_others'] = others
        # expose specific role lists as separate context variables
        context['team_host'] = categories.get('主办律师', [])
        context['team_business_assistant'] = categories.get('律师业务助理', [])
        return context

class TeamMemberPage(Page):
    position = models.CharField(max_length=100)
    ROLE_CHOICES = [
        ('host', '主办律师'),
        ('business_assistant', '律师业务助理'),
    ]
    # 标准化职位枚举，优先使用此字段进行分类；保留 free-text `position` 以兼容历史数据
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, blank=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    bio = RichTextField(blank=True)
    specialties = models.CharField(max_length=255, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('bio'),
        index.SearchField('specialties'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('position'),
        FieldPanel('role'),
        FieldPanel('photo'),
        FieldPanel('specialties'),
        FieldPanel('bio'),
    ]
    
    parent_page_types = ['team.TeamIndexPage']
