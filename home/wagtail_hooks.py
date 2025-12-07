from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models_inquiry import CaseInquiry


class CaseInquiryViewSet(SnippetViewSet):
    model = CaseInquiry
    icon = "doc-full-inverse"
    menu_label = "案情咨询"
    menu_name = "case_inquiries"
    menu_order = 200
    add_to_admin_menu = True
    list_display = ["name", "phone", "created_at", "is_processed"]
    list_filter = ["is_processed", "created_at"]
    search_fields = ["name", "phone", "case_description"]
    ordering = ["-created_at"]


register_snippet(CaseInquiryViewSet)
