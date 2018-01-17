from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from users.models import User
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from utils import constants
import re
from celery_task.tasks import send_active_email

# Create your views here.


# def register(request):
#     """注册"""
#     if request.method == "GET":
#         return render(request, "register.html")
#     else:
#         # post
#         # 接收表单数据，
#         pass


# 类视图  接口 api
class RegisterView(View):
    """注册类视图"""
    def get(self, request):
        """对应get请求方式的逻辑, 返回注册的页面"""
        return render(request, "register.html")

    def post(self, request):
        """对应post请求方式的逻辑"""
        # 获取参数
        # 用户名、密码、确认密码、邮箱、是否同意协议
        user_name = request.POST.get("user_name")  # None
        password = request.POST.get("pwd")
        password2 = request.POST.get("cpwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")

        # 校验参数
        # 逻辑判断  0 0.0 "" [] () {} None False 假
        # all处理所有的元素，只有所有元素都为真，all函数才会返回真，否则返回假
        if not all([user_name, password, password2, email, allow]):
            # 参数不完整
            url = reverse("users:register")
            return redirect(url)

        # 判断两次密码是否一致
        if password != password2:
            return render(request, "register.html", {"errmsg": "两次密码不一致"})

        # 判断邮箱格式是否正确
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}', email):
            # 不匹配
            return render(request, "register.html", {"errmsg": "邮箱格式不正确"})

        # 判断是否勾选了协议
        if allow != "on":
            return render(request, "register.html", {"errmsg": "请同意用户协议"})

        # 业务处理
        # 保存数据到数据库中
        # create_user方法是django用户认证系统提供的，
        # 会帮助我们加密密码并保存到数据库中
        try:
            user = User.objects.create_user(user_name, email, password)
        except IntegrityError as e:
            # 表示用户已注册
            return render(request, "register.html", {"errmsg": "用户名已存在"})

        # 更改用户的激活状态，将默认的已激活改为未激活
        user.is_active = False
        user.save()

        # 生成用户激活的身份token  (令牌）
        token = user.generate_active_token()

        # 拼接激活的连接
        active_url = "http://127.0.0.1:8000/users/active/" + token

        # 发送激活的邮件
        # # send_mail(邮件标题， 邮件内容，发件人， 收件人， html_message=html格式的邮件内容)
        # html_message = """
        # <h1>天天生鲜用户激活</h1>
        # <h2>尊敬的用户%s, 感谢您注册天天生鲜，请在24小时内点击如下链接激活用户</h2>
        # <a href=%s>%s</a>
        # """ % (user_name, active_url, active_url)
        # send_mail("天天生鲜用户激活", "", settings.EMAIL_FROM, [email], html_message=html_message)

        # 异步发送邮件  非阻塞
        send_active_email.delay(user_name, active_url, email)

        # 返回值
        return HttpResponse("这是登录页面")


#
# # 激活邮件
# user_id=4
#
# 请点击这个链接激活用户 http://127.0.0.1:8000/users/active/hfoiwefhoweifhowheofihwofhewoifhoewfhw
#
# 查询字符串  querystring
#
#
# 浏览器  GET 访问  http://http://127.0.0.1:8000/users/active/4 -> 改变用户的激活状态

# 加密计算过程是不能反推的
# 采用签名序列化

class UserActiveView(View):
    """用户激活视图"""
    def get(self, request, user_token):
        """
        用户激活
        :param request:
        :param user_token:  用户激活令牌
        :return:
        """
        # 创建装换工具对象（序列化器）
        s = Serializer(settings.SECRET_KEY, constants.USER_ACTIVE_EXPIRES)
        try:
            data = s.loads(user_token)
        except SignatureExpired:
            # 表示token过期
            return HttpResponse("链接已过期")

        user_id = data.get("user_id")

        # 更新用户的激活状态
        # User.objects.filter(id=user_id).update(is_active=True)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            # 如果不存在，会抛出这个异常
            return HttpResponse("用户不能存在")

        user.is_active = True
        user.save()

        return HttpResponse("这是登录页面")























