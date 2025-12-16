import os
import sys
import django
from pathlib import Path

# Setup Django environment
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawfirm_cms.settings.dev')

import django_tasks.backends.immediate
def dummy_enqueue(*args, **kwargs):
    class DummyResult:
        id = 'dummy'
    return DummyResult()
django_tasks.backends.immediate.ImmediateBackend.enqueue = dummy_enqueue

django.setup()

from service.models import ServiceIndexPage, ServicePage
from wagtail.models import Page

def create_services():
    print("Creating Service Pages...")
    
    # Find the Index Page
    try:
        index_page = ServiceIndexPage.objects.get(slug='yewulingyu')
    except ServiceIndexPage.DoesNotExist:
        print("Service Index Page (slug='yewulingyu') not found. Please create it first.")
        # Try to find home page to create it under
        from home.models import HomePage
        home = HomePage.objects.first()
        if home:
            index_page = ServiceIndexPage(
                title='业务领域',
                slug='yewulingyu',
                intro='核心业务领域'
            )
            home.add_child(instance=index_page)
            index_page.save_revision().publish()
            print("Created Service Index Page.")
        else:
            return

    # List of services to create
    # Format: (Title, Slug, Short Description)
    services = [
        ('刑事法律事务', 'xingshi', '专注于刑事辩护、刑事风险防控及刑事合规业务，为客户提供全方位的刑事法律服务。'),
        ('行政法律事务', 'xingzheng', '代理各类行政复议、行政诉讼案件，维护行政相对人的合法权益，致力于行政争议的实质性解决。'),
        ('商品房集团维权', 'shangpinfang', '专注于商品房买卖合同纠纷、烂尾楼维权、延期交房索赔等群体性案件，保护购房者权益。'),
        ('房地产与建设工程', 'fangdichan', '涵盖土地征收、房屋拆迁、建设工程施工合同纠纷等领域，提供全流程法律服务。'),
        ('资本市场', 'ziben', '为企业上市、并购重组、私募股权投资等资本市场活动提供专业的法律支持与合规建议。'),
        ('公司法律事务', 'gongsi', '提供公司设立、治理机构搭建、股权激励、合同审查等常年法律顾问服务，助力企业稳健发展。'),
        ('民商法律事务', 'minshang', '代理各类民商事诉讼与仲裁案件，包括合同纠纷、侵权纠纷、婚姻家事等，维护当事人合法权益。'),
        ('金融业务', 'jinrong', '服务于银行、保险、信托等金融机构，处理不良资产处置、金融借款合同纠纷等法律事务。'),
    ]

    for title, slug, desc in services:
        if not ServicePage.objects.child_of(index_page).filter(slug=slug).exists():
            page = ServicePage(
                title=title,
                slug=slug,
                short_description=desc,
                body=f'<p>{desc}</p>'
            )
            index_page.add_child(instance=page)
            page.save_revision().publish()
            print(f"Created service: {title}")
        else:
            print(f"Service already exists: {title}")

if __name__ == '__main__':
    create_services()
