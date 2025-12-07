"""更新关于我们页面"""
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

from about.models import AboutPage

about_page = AboutPage.objects.filter(slug='guanyuwomen').first()
if about_page:
    about_page.body = '''<h2>律所简介</h2>
<p style="text-indent: 2em;">北京翰汇律师事务所（原北京吴少博律师事务所）总部位于中国北京，目前以北京为中心，以上海、广州、成都等省会城市和区域中心城市为支点，覆盖全国各大城市群和都市圈，逐步实现专业化、规模化、品牌化发展，联动多家行业机构等资源提升综合法律服务能力，跻身全国一流律所，成为全国不动产纠纷领域实战经验丰富的法律服务新锐品牌机构。</p>

<h2>服务理念</h2>
<p style="text-indent: 2em;"><strong>博思笃行 行法刚正 客户至上 鼎力维权</strong></p>
<p style="text-indent: 2em;">我们始终坚持以客户利益为中心，以专业、敬业、正直的态度，为每一位当事人提供优质的法律服务。</p>

<h2>核心业务</h2>
<p style="text-indent: 2em;">• 征地拆迁法律服务</p>
<p style="text-indent: 2em;">• 商品房群体维权</p>
<p style="text-indent: 2em;">• 行政争议解决</p>
<p style="text-indent: 2em;">• 企业法律顾问</p>
<p style="text-indent: 2em;">• 房地产纠纷代理</p>

<h2>联系方式</h2>
<p style="text-indent: 2em;">地址：北京市丰台区金泽路161号悦中心22层2208室</p>
<p style="text-indent: 2em;">电话：400-155-0888</p>'''
    about_page.save_revision().publish()
    print('关于我们页面更新成功')
else:
    print('找不到页面')
