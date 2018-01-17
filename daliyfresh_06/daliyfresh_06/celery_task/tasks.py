from celery import Celery
import os

os.environ["DJANGO_SETTING_MODULE"] = "daliafresh_06.settings"
# 在启动celery的时候需要，在django启动时不需要，注释
# 手动初始化django，读入配置文件

# import django
# django.setup()

from django.conf import settings
from django.core.mail import send_mail

# 创建celery的应用
app = Celery("dailyfresh", broker="redis://IP地址/6379/0")


# 定义任务

@app.task
def send_active_email(user_name, active_url, email):
    """发送激活邮件"""
    # 发送激活的邮件
    # send_mail (邮件标题，邮件内容，发件人，收件人，html_message=html格式)
    html_message = """
                <h1>天天生鲜用户激活</h1>
                <h2>尊敬的用户%s, 感谢您注册天天生鲜，请在24小时内点击如下链接激活用户</h2>
                <a href=%s>%s</a>
                """ % (user_name, active_url, active_url)
    send_mail("天天生鲜用户激活", "", settings.EMAIL_FROM, [email], html_message=html_message)
