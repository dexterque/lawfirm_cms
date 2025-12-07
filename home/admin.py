from django.contrib import admin
from .models_inquiry import CaseInquiry


@admin.register(CaseInquiry)
class CaseInquiryAdmin(admin.ModelAdmin):
    """案情咨询后台管理"""
    list_display = ('name', 'phone', 'case_description_short', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'phone', 'case_description')
    ordering = ['-created_at']
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('咨询信息', {
            'fields': ('name', 'phone', 'case_description', 'created_at')
        }),
        ('处理状态', {
            'fields': ('is_processed', 'notes')
        }),
    )
    
    def case_description_short(self, obj):
        if len(obj.case_description) > 50:
            return obj.case_description[:50] + '...'
        return obj.case_description
    case_description_short.short_description = '案情描述'
