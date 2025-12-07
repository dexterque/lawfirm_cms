"""
自动从静态页面导入初始内容到Wagtail CMS
"""
import os
import sys
import re
from datetime import date
from pathlib import Path
from html.parser import HTMLParser

# 设置Django环境
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lawfirm_cms.settings.dev')

# Monkeypatch to fix django_tasks issue
import django_tasks.backends.immediate
def dummy_enqueue(*args, **kwargs):
    class DummyResult:
        id = 'dummy'
    return DummyResult()
django_tasks.backends.immediate.ImmediateBackend.enqueue = dummy_enqueue

import django
django.setup()

from django.utils.html import strip_tags
from wagtail.models import Page
from home.models import HomePage
from article.models import ArticleIndexPage, ArticlePage
from team.models import TeamIndexPage, TeamMemberPage
from about.models import AboutPage


class HTMLContentParser(HTMLParser):
    """解析HTML内容"""
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_content = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ['p', 'div']:
            self.in_content = True
            
    def handle_endtag(self, tag):
        if tag in ['p', 'div']:
            self.in_content = False
            
    def handle_data(self, data):
        if self.in_content:
            self.text.append(data.strip())
            
    def get_text(self):
        return ' '.join(filter(None, self.text))


def extract_title_from_html(html_content):
    """从HTML提取标题"""
    match = re.search(r'<title>([^<]+)</title>', html_content)
    if match:
        title = match.group(1).replace('_翰汇所', '').strip()
        return title
    return None


def extract_date_from_html(html_content):
    """从HTML提取日期"""
    match = re.search(r'发布时间[：:](\d{4}-\d{2}-\d{2})', html_content)
    if match:
        date_str = match.group(1)
        parts = date_str.split('-')
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    return date.today()


def extract_body_from_html(html_content):
    """从HTML提取正文内容"""
    # 找到NyNewDetail_Content内容
    match = re.search(r'<div class="NyNewDetail_Content">\s*(.*?)\s*</div>\s*<div class="shangxia">', 
                     html_content, re.DOTALL)
    if match:
        body = match.group(1)
        # 处理图片路径
        body = re.sub(r'src="\.\./', 'src="/', body)
        body = re.sub(r'src="uploads/', 'src="/uploads/', body)
        return body
    return ""


def create_news_articles():
    """创建新闻动态文章"""
    print("创建新闻动态文章...")
    
    news_index = ArticleIndexPage.objects.filter(slug='xinwendongtai').first()
    if not news_index:
        print("找不到新闻动态索引页")
        return
    
    # 检查是否已有文章
    existing_count = ArticlePage.objects.child_of(news_index).count()
    if existing_count >= 3:
        print(f"新闻动态已有 {existing_count} 篇文章，跳过")
        return
    
    # 新闻数据
    news_data = [
        {
            'title': '双奖加身 翰汇律所闪耀第十届桂客年会 专精铸业公益铸魂',
            'slug': 'news-2240',
            'date': date(2025, 11, 12),
            'intro': '2025年11月8日，第十届桂客年会在北京国家会议中心隆重启幕。本届年会以"对标未来：走向国际一流律所的中国律师业"为主题，汇聚全国法律界领军人物。',
            'body': '''<p style="text-indent: 2em;">2025年11月8日，第十届桂客年会在北京国家会议中心隆重启幕。本届年会以"对标未来：走向国际一流律所的中国律师业"为主题，汇聚全国法律界领军人物、业界精英与学界翘楚，共探行业国际化转型新路径。</p>
<p style="text-indent: 2em;">盛典现场，北京翰汇律师事务所凭借在专业领域的深耕突破与公益领域的持续践行，斩获"团队专精特新奖"，律所主任吴少博荣膺"公益至善奖"，双项荣誉彰显行业对其专业实力与社会责任的双重认可。</p>
<p style="text-indent: 2em;">作为贯穿行发展金十年的权威盛会，桂客年会的奖项评选聚焦专业化、特色化、创新性与社会价值，是中国律师业高质量发展的重要风向标。此次翰汇律所获评"团队专精特新奖"，源于其长期扎根房地产、行政争议、企业破产等核心领域的深耕细作，以及在服务模式上的持续创新。</p>
<p style="text-indent: 2em;">"双奖加身是荣誉更是鞭策，" 吴少博主任表示，"翰汇律所将以此次获奖为契机，继续深耕专业领域，持续创新服务模式，同时坚守公益初心，在'法商融合'的发展道路上，既做企业发展的法治护航者，也做民生权益的坚定守护者，向国际一流律所的目标稳步迈进。"</p>'''
        },
        {
            'title': '丰台法务区房地产法律研究中心揭牌暨北京翰汇律所十周年庆成功举行',
            'slug': 'news-2234',
            'date': date(2025, 11, 10),
            'intro': '近日，"丰台法务区房地产法律研究中心揭牌仪式暨北京翰汇律师事务所十周年庆"活动在京顺利举办。',
            'body': '''<p style="text-indent: 2em;">近日，"丰台法务区房地产法律研究中心揭牌仪式暨北京翰汇律师事务所十周年庆"活动在京顺利举办。活动以"法治赋能促发展 协同共建新格局"为主题，汇聚政府部门、高校学者、行业专家及媒体代表，共同见证翰汇律所十年发展历程，并就房地产法律服务领域的未来发展展开深入交流。</p>
<p style="text-indent: 2em;">活动现场，丰台法务区房地产法律研究中心正式揭牌成立。该中心由北京翰汇律师事务所牵头组建，旨在整合法律研究与实务资源，聚焦房地产领域法律问题，为政府决策、企业发展和公众权益保护提供专业支持。</p>
<p style="text-indent: 2em;">翰汇律所主任吴少博在致辞中表示，十年来，翰汇律所始终秉持"博思笃行 行法刚正 客户至上 鼎力维权"的理念，从最初的小团队发展成为在房地产、行政争议等领域具有影响力的专业律所。未来，律所将继续深耕专业领域，以研究中心为平台，推动行业交流与合作，为法治中国建设贡献力量。</p>'''
        },
        {
            'title': '关于警惕冒充翰汇律所人员诈骗行为的声明',
            'slug': 'news-1991',
            'date': date(2025, 6, 9),
            'intro': '近期，我所发现有不法分子冒充翰汇律师事务所工作人员实施诈骗行为，特此发布声明提醒广大群众提高警惕。',
            'body': '''<p style="text-indent: 2em;">近期，我所发现有不法分子冒充北京翰汇律师事务所工作人员，通过电话、微信等方式联系当事人，以"案件代理""法律咨询""退费返款"等名义实施诈骗行为。</p>
<p style="text-indent: 2em;">为维护广大群众合法权益，北京翰汇律师事务所特此声明：</p>
<p style="text-indent: 2em;">1、我所从未委托任何第三方机构或个人以我所名义对外进行业务推广或收取费用；</p>
<p style="text-indent: 2em;">2、我所正式工作人员均持有律师执业证或法律职业资格证，可通过官方渠道核实身份；</p>
<p style="text-indent: 2em;">3、如遇可疑情况，请立即拨打我所官方电话400-155-0888进行核实；</p>
<p style="text-indent: 2em;">4、如发现被骗，请立即向当地公安机关报案。</p>
<p style="text-indent: 2em;">感谢社会各界对北京翰汇律师事务所的信任与支持！</p>'''
        },
    ]
    
    for data in news_data:
        if not ArticlePage.objects.filter(slug=data['slug']).exists():
            article = ArticlePage(
                title=data['title'],
                slug=data['slug'],
                date=data['date'],
                intro=data['intro'],
                body=data['body']
            )
            news_index.add_child(instance=article)
            article.save_revision().publish()
            print(f"  创建文章: {data['title']}")


def create_case_articles():
    """创建经典案例文章"""
    print("创建经典案例文章...")
    
    cases_index = ArticleIndexPage.objects.filter(slug='jingdiananli').first()
    if not cases_index:
        print("找不到经典案例索引页")
        return
    
    existing_count = ArticlePage.objects.child_of(cases_index).count()
    if existing_count >= 3:
        print(f"经典案例已有 {existing_count} 篇文章，跳过")
        return
    
    cases_data = [
        {
            'title': '胜诉 | 养牛场关停补偿遇阻三年维权路 律师直击行政瑕疵终胜诉',
            'slug': 'case-2265',
            'date': date(2025, 12, 4),
            'intro': '当事人经营的养牛场因环保政策被关停，但补偿款迟迟未能到位。在翰汇律所的代理下，通过行政诉讼途径，最终赢得胜诉。',
            'body': '''<p style="text-indent: 2em;">【案情简介】</p>
<p style="text-indent: 2em;">当事人张某在某县经营养牛场多年，2022年因当地环保整治政策被要求关停。然而，承诺的补偿款却迟迟未能兑现。张某多次与相关部门沟通无果，无奈之下委托北京翰汇律师事务所代理此案。</p>
<p style="text-indent: 2em;">【代理过程】</p>
<p style="text-indent: 2em;">律师接案后，首先对案件进行了全面分析，发现相关部门在关停程序中存在多处行政瑕疵：未依法进行听证、未出具正式的关停决定书、补偿标准未经法定程序确定。</p>
<p style="text-indent: 2em;">基于上述问题，律师制定了"行政复议+行政诉讼"的双轨维权策略。</p>
<p style="text-indent: 2em;">【案件结果】</p>
<p style="text-indent: 2em;">经过近一年的诉讼，法院最终判决相关部门的关停行为违法，并责令其在判决生效后60日内依法作出补偿决定。当事人成功获得应有的补偿。</p>'''
        },
        {
            'title': '胜诉 | 预告登记下的房权之争 律师力证真实交易 助业主保住房产',
            'slug': 'case-2263',
            'date': date(2025, 12, 2),
            'intro': '业主购买的商品房遭遇开发商债权人查封，翰汇律师通过充分举证，成功保住了业主的房产权益。',
            'body': '''<p style="text-indent: 2em;">【案情简介】</p>
<p style="text-indent: 2em;">王女士于2020年购买了某楼盘的商品房一套，并办理了预告登记。然而，2023年该开发商因债务纠纷被起诉，债权人申请查封了包括王女士所购房屋在内的多套房产。</p>
<p style="text-indent: 2em;">【代理过程】</p>
<p style="text-indent: 2em;">翰汇律所接受委托后，立即着手收集证据，包括购房合同、付款凭证、预告登记证明、物业费缴纳记录等，充分证明王女士是善意购房人，交易真实有效。</p>
<p style="text-indent: 2em;">【案件结果】</p>
<p style="text-indent: 2em;">法院经审理认为，王女士在查封前已签订购房合同并支付全部房款，且已办理预告登记并实际占有房屋，符合法定的物权保护条件。最终判决解除对涉案房屋的查封，王女士成功保住了自己的房产。</p>'''
        },
        {
            'title': '成果 | 商品房停滞维权 律师借力复议助业主成功退房退款',
            'slug': 'case-2262',
            'date': date(2025, 12, 1),
            'intro': '业主购买的商品房项目停工烂尾，在翰汇律所的帮助下，通过行政复议途径成功实现退房退款。',
            'body': '''<p style="text-indent: 2em;">【案情简介】</p>
<p style="text-indent: 2em;">李先生于2021年购买了某楼盘的期房，原定2023年交付。然而，该项目于2022年底停工至今，开发商无力继续建设。李先生多次要求退房退款，均遭到开发商拒绝。</p>
<p style="text-indent: 2em;">【代理过程】</p>
<p style="text-indent: 2em;">翰汇律所律师分析案情后，发现该项目在预售许可、资金监管等方面存在违规问题。律师决定从行政监管角度切入，向相关部门提起行政复议，要求其履行监管职责。</p>
<p style="text-indent: 2em;">【案件结果】</p>
<p style="text-indent: 2em;">在行政复议压力下，相关部门介入协调。最终，开发商同意退还李先生全部购房款及利息，双方达成和解。</p>'''
        },
    ]
    
    for data in cases_data:
        if not ArticlePage.objects.filter(slug=data['slug']).exists():
            article = ArticlePage(
                title=data['title'],
                slug=data['slug'],
                date=data['date'],
                intro=data['intro'],
                body=data['body']
            )
            cases_index.add_child(instance=article)
            article.save_revision().publish()
            print(f"  创建案例: {data['title']}")


def create_knowledge_articles():
    """创建知识课堂文章"""
    print("创建知识课堂文章...")
    
    knowledge_index = ArticleIndexPage.objects.filter(slug='zhishiketang').first()
    if not knowledge_index:
        print("找不到知识课堂索引页")
        return
    
    existing_count = ArticlePage.objects.child_of(knowledge_index).count()
    if existing_count >= 3:
        print(f"知识课堂已有 {existing_count} 篇文章，跳过")
        return
    
    knowledge_data = [
        {
            'title': '遭遇违法强拆别乱慌 取证维权有章法',
            'slug': 'knowledge-2261',
            'date': date(2025, 11, 28),
            'intro': '面对违法强拆，如何有效取证并依法维权？本文为您详细解读。',
            'body': '''<p style="text-indent: 2em;">房屋遭遇强拆，很多当事人往往慌了手脚，不知所措。其实，只要掌握正确的方法，依法维权并非难事。</p>
<p style="text-indent: 2em;"><strong>一、保持冷静，确保人身安全</strong></p>
<p style="text-indent: 2em;">强拆发生时，首先要确保自身和家人的人身安全，不要与强拆人员发生肢体冲突。</p>
<p style="text-indent: 2em;"><strong>二、及时取证</strong></p>
<p style="text-indent: 2em;">1. 用手机录像，记录强拆过程、参与人员、车辆等信息；</p>
<p style="text-indent: 2em;">2. 拍照保存强拆前后的房屋状况对比；</p>
<p style="text-indent: 2em;">3. 记录强拆时间、地点等基本信息；</p>
<p style="text-indent: 2em;">4. 保留好房产证、土地证等权属证明。</p>
<p style="text-indent: 2em;"><strong>三、及时报警</strong></p>
<p style="text-indent: 2em;">拨打110报警，要求警方出警并做好笔录，保留报警回执。</p>
<p style="text-indent: 2em;"><strong>四、尽快咨询专业律师</strong></p>
<p style="text-indent: 2em;">在法定期限内提起行政复议或行政诉讼，维护自身合法权益。</p>'''
        },
        {
            'title': '退林还耕避坑指南 从签字到领补全说清',
            'slug': 'knowledge-2260',
            'date': date(2025, 11, 26),
            'intro': '退林还耕政策涉及农民切身利益，如何避免常见的坑，本文为您详细解读。',
            'body': '''<p style="text-indent: 2em;">近年来，各地积极推进退林还耕工作，但在实施过程中，一些农户因不了解政策而吃亏。以下是常见的几个"坑"及应对方法：</p>
<p style="text-indent: 2em;"><strong>一、不要轻易签字</strong></p>
<p style="text-indent: 2em;">签字前一定要仔细阅读协议内容，特别是补偿标准、支付时间、违约责任等条款。</p>
<p style="text-indent: 2em;"><strong>二、了解补偿标准</strong></p>
<p style="text-indent: 2em;">退林还耕的补偿通常包括林木补偿、地上附着物补偿、青苗补偿等，要了解当地的具体标准。</p>
<p style="text-indent: 2em;"><strong>三、保留证据</strong></p>
<p style="text-indent: 2em;">对林地面积、林木数量、地上附着物等进行拍照记录，作为日后维权的证据。</p>
<p style="text-indent: 2em;"><strong>四、先补后征</strong></p>
<p style="text-indent: 2em;">根据法律规定，应当先落实补偿再实施征收，切勿在未拿到补偿款的情况下交出林地。</p>'''
        },
        {
            'title': '商铺返租 四大陷阱要警惕',
            'slug': 'knowledge-2259',
            'date': date(2025, 11, 25),
            'intro': '商铺返租看似稳赚不赔，实则暗藏风险。本文揭示四大常见陷阱。',
            'body': '''<p style="text-indent: 2em;">商铺返租，即开发商在销售商铺时承诺固定收益回报，由开发商统一经营管理。这种模式看似诱人，实则风险重重。</p>
<p style="text-indent: 2em;"><strong>陷阱一：虚假宣传高回报</strong></p>
<p style="text-indent: 2em;">部分开发商承诺年化收益8%-12%甚至更高，远超市场合理水平，后期往往难以兑现。</p>
<p style="text-indent: 2em;"><strong>陷阱二：合同条款有猫腻</strong></p>
<p style="text-indent: 2em;">返租合同中可能存在收益递减、提前解约等不利条款，签约前务必仔细审查。</p>
<p style="text-indent: 2em;"><strong>陷阱三：产权分割有风险</strong></p>
<p style="text-indent: 2em;">部分商铺采用分割销售模式，单个商铺面积很小，日后难以独立经营。</p>
<p style="text-indent: 2em;"><strong>陷阱四：开发商跑路</strong></p>
<p style="text-indent: 2em;">一旦开发商经营不善或恶意跑路，返租收益将化为泡影。</p>
<p style="text-indent: 2em;"><strong>建议：</strong>购买商铺前，务必对开发商资质、项目前景进行充分调查，谨慎决策。</p>'''
        },
    ]
    
    for data in knowledge_data:
        if not ArticlePage.objects.filter(slug=data['slug']).exists():
            article = ArticlePage(
                title=data['title'],
                slug=data['slug'],
                date=data['date'],
                intro=data['intro'],
                body=data['body']
            )
            knowledge_index.add_child(instance=article)
            article.save_revision().publish()
            print(f"  创建文章: {data['title']}")


def create_team_members():
    """创建团队成员"""
    print("创建团队成员...")
    
    team_index = TeamIndexPage.objects.filter(slug='zhuanyetuandui').first()
    if not team_index:
        print("找不到专业团队索引页")
        return
    
    existing_count = TeamMemberPage.objects.child_of(team_index).count()
    if existing_count >= 3:
        print(f"专业团队已有 {existing_count} 名成员，跳过")
        return
    
    team_data = [
        {
            'title': '吴少博',
            'slug': 'lawyer-wushaobo',
            'position': '创始人、主任律师',
            'specialties': '房地产纠纷、行政争议、企业法律顾问',
            'bio': '''<p>吴少博律师，北京翰汇律师事务所创始人、主任。中国政法大学法学硕士，从事法律工作二十余年，在房地产纠纷、征地拆迁、行政争议等领域积累了丰富的实务经验。</p>
<p>曾成功代理多起重大房地产群体性案件，为数百名业主挽回经济损失。秉持"博思笃行 行法刚正 客户至上 鼎力维权"的执业理念，以专业、敬业、正直的态度服务每一位当事人。</p>
<p>社会职务：北京市律师协会房地产法律专业委员会委员、中国法学会会员。</p>'''
        },
        {
            'title': '宋府育',
            'slug': 'lawyer-songfuyu',
            'position': '合伙人律师',
            'specialties': '征地拆迁、行政诉讼、商事仲裁',
            'bio': '''<p>宋府育律师，北京翰汇律师事务所合伙人。法学本科学历，具有多年法律从业经验，擅长征地拆迁、行政诉讼、商事仲裁等领域。</p>
<p>曾参与办理多起涉及集体土地征收、国有土地上房屋征收的案件，为当事人争取到合理补偿。工作细致认真，善于从复杂案情中理清法律关系，制定有效的诉讼策略。</p>'''
        },
        {
            'title': '石磊',
            'slug': 'lawyer-shilei',
            'position': '专职律师',
            'specialties': '房屋买卖纠纷、物业纠纷、合同纠纷',
            'bio': '''<p>石磊律师，北京翰汇律师事务所专职律师。法学硕士学位，专注于房屋买卖纠纷、物业纠纷、合同纠纷等民商事领域。</p>
<p>具有扎实的法学理论基础和丰富的实务经验，曾成功代理多起商品房质量纠纷、物业服务合同纠纷案件。工作认真负责，能够站在当事人角度思考问题，提供切实可行的法律解决方案。</p>'''
        },
    ]
    
    for data in team_data:
        if not TeamMemberPage.objects.filter(slug=data['slug']).exists():
            member = TeamMemberPage(
                title=data['title'],
                slug=data['slug'],
                position=data['position'],
                specialties=data['specialties'],
                bio=data['bio']
            )
            team_index.add_child(instance=member)
            member.save_revision().publish()
            print(f"  创建成员: {data['title']}")


def update_about_page():
    """更新关于我们页面内容"""
    print("更新关于我们页面...")
    
    about_page = AboutPage.objects.filter(slug='guanyuwomen').first()
    if not about_page:
        print("找不到关于我们页面")
        return
    
    if about_page.body:
        print("关于我们页面已有内容，跳过")
        return
    
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
<p style="text-indent: 2em;">电话：400-155-0888</p>
<p style="text-indent: 2em;">邮箱：info@wushaobolawfirm.com</p>'''
    
    about_page.save_revision().publish()
    print("  更新完成")


def main():
    print("=" * 50)
    print("开始导入初始内容...")
    print("=" * 50)
    
    create_news_articles()
    create_case_articles()
    create_knowledge_articles()
    create_team_members()
    update_about_page()
    
    print("=" * 50)
    print("内容导入完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()
