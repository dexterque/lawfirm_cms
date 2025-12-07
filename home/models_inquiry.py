from django.db import models
from django.core.validators import RegexValidator


class CaseInquiry(models.Model):
    """案情咨询信息"""
    name = models.CharField(max_length=100, verbose_name="姓名")
    phone = models.CharField(
        max_length=11, 
        verbose_name="手机号码",
        validators=[
            RegexValidator(
                regex=r'^1[3-9]\d{9}$',
                message='请输入有效的手机号码'
            )
        ]
    )
    case_description = models.TextField(verbose_name="案情描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")
    is_processed = models.BooleanField(default=False, verbose_name="是否已处理")
    notes = models.TextField(blank=True, verbose_name="处理备注")
    
    class Meta:
        verbose_name = "案情咨询"
        verbose_name_plural = "案情咨询"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.phone} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
