# Law Firm CMS 部署指南 (Ubuntu)

基于 Django 5 + Wagtail 的律所官网/内容管理系统，代码位于 `lawfirm_cms/` 目录。下文以 Ubuntu 20.04/22.04 为例说明从零到上线的流程。

## 环境要求
- Python 3.10+（推荐与 Dockerfile 一致的 3.12）
- pip / venv
- SQLite 默认即可；如需 PostgreSQL 请在 `settings/local.py` 中调整 `DATABASES`
- 可选：Node.js（仅在重新编译 Tailwind 时需要）

## 生产环境配置（必须）
在 `lawfirm_cms/lawfirm_cms/settings/local.py` 新建文件，填入至少以下内容：
```python
SECRET_KEY = "请替换为强随机字符串"
ALLOWED_HOSTS = ["your-domain.com", "服务器IP"]
# 如果改用 PostgreSQL，配置 DATABASES 并安装 libpq-dev、psycopg2-binary
```
生产启动时务必设置环境变量 `DJANGO_SETTINGS_MODULE=lawfirm_cms.settings.production`。

## 部署步骤（非 Docker）
1) 系统依赖  
   ```bash
   sudo apt update
   sudo apt install -y python3-venv python3-dev build-essential libpq-dev libjpeg-dev zlib1g-dev libwebp-dev
   ```
2) 获取代码  
   ```bash
   git clone <your_repo_url> laws
   cd laws/lawfirm_cms
   ```
3) 创建虚拟环境并安装依赖  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4) 数据库迁移与静态资源  
   ```bash
   export DJANGO_SETTINGS_MODULE=lawfirm_cms.settings.production
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
5) 创建后台管理员  
   ```bash
   python manage.py createsuperuser
   ```
6) 启动应用  
   开发验证：`python manage.py runserver 0.0.0.0:8000 --settings=lawfirm_cms.settings.production`  
   正式环境（推荐）：  
   ```bash
   gunicorn lawfirm_cms.wsgi:application \
     --bind 0.0.0.0:8000 \
     --env DJANGO_SETTINGS_MODULE=lawfirm_cms.settings.production
   ```

## systemd 示例（可选）
将下述内容保存到 `/etc/systemd/system/lawfirm-cms.service`，并根据实际路径调整：
```ini
[Unit]
Description=Law Firm CMS
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/laws/lawfirm_cms
Environment="DJANGO_SETTINGS_MODULE=lawfirm_cms.settings.production"
Environment="PATH=/opt/laws/lawfirm_cms/.venv/bin"
ExecStart=/opt/laws/lawfirm_cms/.venv/bin/gunicorn lawfirm_cms.wsgi:application --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```
启动并自启：`sudo systemctl enable --now lawfirm-cms`.

## Nginx 反向代理（示例）
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /opt/laws/lawfirm_cms/static/;
    }
    location /media/ {
        alias /opt/laws/lawfirm_cms/media/;
    }
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Docker 部署（可选）
在仓库根目录执行：
```bash
cd lawfirm_cms
docker build -t lawfirm-cms .
docker run -d --name lawfirm-cms -p 8000:8000 \
  -e DJANGO_SETTINGS_MODULE=lawfirm_cms.settings.production \
  -v /srv/lawfirm_cms/static:/app/static \
  -v /srv/lawfirm_cms/media:/app/media \
  lawfirm-cms
```
仍需在容器中或通过挂载方式提供 `settings/local.py` 以设置 `SECRET_KEY` 和 `ALLOWED_HOSTS`。

## 目录提示
- 业务与页面代码：`lawfirm_cms/`（Django/Wagtail 项目）
- 静态文件输出：`lawfirm_cms/static/`
- 上传媒体：`lawfirm_cms/media/`
- 初始内容脚本：`create_initial_content.py`、`import_content.py` 等，可在迁移后按需运行

完成上述步骤后，即可通过 Nginx 访问上线的 Wagtail 后台与前台站点。***
