# Law Firm CMS

律所内容管理系统，基于 Django + Wagtail 构建。

## Ubuntu 简易部署指南

以下步骤适用于 Ubuntu 20.04/22.04/24.04。

### 1. 安装基础环境

首先更新系统并安装必要的 Python 和 Nginx 组件：

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip python3-dev nginx git
```

### 2. 获取代码与安装依赖

建议将代码放在 `/var/www/` 或用户主目录下。

```bash
# 1. 下载代码 (请替换为实际仓库地址)
git clone <你的仓库地址> lawfirm_cms
cd lawfirm_cms

# 2. 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装项目依赖
pip install -r requirements.txt

# 4. 安装生产应用服务器 (requirements.txt 中未包含)
pip install gunicorn
```

### 3. 项目配置

在 `lawfirm_cms/settings/` 目录下创建 `local.py` 文件，填入生产环境配置：

`nano lawfirm_cms/settings/local.py`

```python
from .base import *

# !!! 必须修改为独特的随机字符串 !!!
SECRET_KEY = 'change-me-to-a-secure-random-secret-key'

# 允许访问的域名和IP
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', '服务器公网IP']

DEBUG = False
```

### 4. 初始化数据

```bash
# 收集静态文件 (CSS/JS)
python manage.py collectstatic --noinput

# 创建数据库表
python manage.py migrate

# 创建后台管理员账号
python manage.py createsuperuser
```

### 5. 启动服务 (使用 Gunicorn)

我们使用 Systemd 来管理服务，确保它在后台运行并在开机时自动启动。

创建服务文件：
`sudo nano /etc/systemd/system/lawfirm.service`

写入以下内容（**注意修改路径**）：

```ini
[Unit]
Description=Law Firm CMS Gunicorn Daemon
After=network.target

[Service]
# 运行用户，通常推荐使用当前用户或 www-data
User=root
# 项目所在目录 (请修改为实际路径!)
WorkingDirectory=/root/lawfirm_cms
# Gunicorn 命令路径 (在虚拟环境中)
ExecStart=/root/lawfirm_cms/venv/bin/gunicorn lawfirm_cms.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

启动并设置开机自启：
```bash
sudo systemctl start lawfirm
sudo systemctl enable lawfirm
```

### 6. 配置 Nginx (对外发布)

配置 Nginx 处理静态文件并将流量转发到 Gunicorn。

创建配置文件：
`sudo nano /etc/nginx/sites-available/lawfirm`

```nginx
server {
    listen 80;
    server_name yourdomain.com; # 替换域名或IP

    # 静态文件路径 (请修改为实际路径!)
    location /static/ {
        alias /root/lawfirm_cms/static/;
    }

    # 媒体文件路径 (上传的图片等)
    location /media/ {
        alias /root/lawfirm_cms/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

启用配置并重启 Nginx：
```bash
sudo ln -s /etc/nginx/sites-available/lawfirm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

部署完成！访问你的域名即可看到网站。
