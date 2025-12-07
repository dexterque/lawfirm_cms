import json
import re
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models_inquiry import CaseInquiry


def validate_phone(phone):
    """验证手机号格式"""
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))


@csrf_protect
@require_POST
def submit_case_inquiry(request):
    """处理案情咨询提交"""
    try:
        # 获取表单数据
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        case_description = request.POST.get('case_description', '').strip()
        
        # 验证必填字段
        errors = {}
        
        if not name:
            errors['name'] = '请输入您的姓名'
        elif len(name) > 100:
            errors['name'] = '姓名长度不能超过100个字符'
            
        if not phone:
            errors['phone'] = '请输入您的手机号码'
        elif not validate_phone(phone):
            errors['phone'] = '请输入有效的11位手机号码'
            
        if not case_description:
            errors['case_description'] = '请输入您的案情描述'
        elif len(case_description) > 2000:
            errors['case_description'] = '案情描述不能超过2000个字符'
        
        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': '请检查输入信息'
            }, status=400)
        
        # 保存到数据库
        inquiry = CaseInquiry.objects.create(
            name=name,
            phone=phone,
            case_description=case_description
        )
        
        return JsonResponse({
            'success': True,
            'message': '提交成功！我们的律师会尽快与您联系。',
            'inquiry_id': inquiry.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': '提交失败，请稍后重试。',
            'error': str(e)
        }, status=500)
