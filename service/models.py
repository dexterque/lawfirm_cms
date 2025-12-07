from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

class ServiceIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    subpage_types = ['service.ServicePage']
    
    def get_context(self, request):
        context = super().get_context(request)
        # 获取具体的 ServicePage 实例
        services = ServicePage.objects.child_of(self).live().order_by('first_published_at')
        context['services'] = services
        return context

class ServicePage(Page):
    icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    short_description = models.CharField(max_length=255)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('icon'),
        FieldPanel('short_description'),
        FieldPanel('body'),
    ]
    
    parent_page_types = ['service.ServiceIndexPage']
