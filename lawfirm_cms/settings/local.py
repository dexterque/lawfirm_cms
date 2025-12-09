# Production overrides (do not commit real secrets to VCS).

# 必填：生产环境随机密钥
SECRET_KEY = "replace-with-strong-random-string"

# 必填：允许访问的域名 / IP
ALLOWED_HOSTS = ["your-domain.com", "144.168.60.233"]

# 如需改用 PostgreSQL，可取消注释并填写实际参数
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "your_db_name",
#         "USER": "your_db_user",
#         "PASSWORD": "your_db_password",
#         "HOST": "127.0.0.1",
#         "PORT": "5432",
#     }
# }

