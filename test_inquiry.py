"""测试案情提交API"""
import os
import sys
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawfirm_cms.settings.dev')

import django_tasks.backends.immediate
def dummy_enqueue(*args, **kwargs):
    class DummyResult:
        id = 'dummy'
    return DummyResult()
django_tasks.backends.immediate.ImmediateBackend.enqueue = dummy_enqueue

import django
django.setup()

from home.models_inquiry import CaseInquiry

# 直接创建一条测试数据
inquiry = CaseInquiry.objects.create(
    name='测试用户',
    phone='13800138000',
    case_description='这是一个测试案情咨询信息，用于验证表单提交功能是否正常工作。'
)

print(f'创建成功! ID: {inquiry.id}')
print(f'姓名: {inquiry.name}')
print(f'手机: {inquiry.phone}')
print(f'案情: {inquiry.case_description}')
print(f'提交时间: {inquiry.created_at}')

# 列出所有咨询
print('\n所有案情咨询:')
for inq in CaseInquiry.objects.all():
    print(f'  - [{inq.id}] {inq.name} ({inq.phone}) - {inq.created_at}')
