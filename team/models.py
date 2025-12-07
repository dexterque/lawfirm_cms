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
        context['members'] = members
        context['members_with_photo'] = members.exclude(photo__isnull=True)
        return context

class TeamMemberPage(Page):
    position = models.CharField(max_length=100)
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
        FieldPanel('photo'),
        FieldPanel('specialties'),
        FieldPanel('bio'),
    ]
    
    parent_page_types = ['team.TeamIndexPage']
