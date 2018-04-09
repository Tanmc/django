[TOC]



# Django项目

## 1.项目架构

### 前端部分

```前端部分
用户页面，商品页面，购物车页面，订单页面，运营后台页面
```

### 后端部分

```后端部分
用户， 商品， 购物车， 订单，搜索
```

### 数据库部分

```数据部分
MySQL mysql主从同步/双击热备
redis session服务器 缓存服务器
celery 异步服务
FastDFS 分布式文件服务
```



## 2.数据库表结构

### 1.用户表

```用户表

```

### 2.地址表

```


```

### 3.首页分类商品表

```

```

### 4.首页轮播商品表

```
以空间换时间
```

### 5.首页活动表

```

```

### 6.商品SKU表

```

```

#### SKU=stock keeping unit（库存量单位）

```
sku级库存进出计量单位，可以使见，和，托盘为单位
sku是物理上不可分割的最小存货单元，根据不同业态，不同管理模式来处理，例如服装sku表示：规格，颜色，款式
```

### 7.商品SPU表

#### SPU=StandardProduct Unit(标准产品单位)

```
spu是描述商品信息聚合的最小单位，可复用性，易检索的标准化信息的集合，商品属性值，特性相同的商品称为spu
```

### 8.类别表

```

```

### 9.图片表

```

```

### 10.订单表

```

```

### 11.订单商品表

```

```

## 3.数据库读写分离

### Ubuntu

```
MySQL 主mastar  写
```

### Windows

```
MySQL 从slave  读
```

## 3.1创建项目

```
django-admin startproject  #项目名称 
django-admin startproject dailyfresh_06  
```

接下来可以使用IDE打开此目录，开发项目了，此处使用pycharm打开dailyfresh_06目录。

#### 项目默认目录说明

```
manage.py是项目管理文件，通过它管理项目。
与项目同名的目录，此处为test1。
_init_.py是一个空文件，作用是这个目录test1可以被当作包使用。
settings.py是项目的整体配置文件。
urls.py是项目的URL配置文件。
wsgi.py是项目与WSGI兼容的Web服务器入口，详细内容会在布署中讲到
```

#### 创建应用

```
python manage.py startapp #应用名称
python manage.py startapp apps
```

#### 应用默认目录说明

```
_init.py_是一个空文件，表示当前目录appst可以当作一个python包使用。
tests.py文件用于开发测试用例，在实际开发中会有专门的测试人员，这个事情不需要我们来做。
models.py文件跟数据库操作相关。
views.py文件跟接收浏览器请求，进行处理，返回页面相关。
admin.py文件跟网站的后台管理相关。
migrations文件夹之后给大家介绍
```

#### 安装应用

```
应用创建成功后，需要安装才可以使用，也就是建立应用和项目之间的关联，在dailyfresh_06/settings.py中INSTALLED_APPS下添加应用的名称就可以完成安装。
接下来在元组中添加一个新的项 apps，
初始项目的INSTALLED_APPS如下：
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps',
    )
```

#### 开发服务器

```
在开发阶段，为了能够快速预览到开发的效果，django提供了一个纯python编写的轻量级web服务器，仅在开发阶段使用。

运行服务器命令如下：

python manage.py runserver ip:端口
例：
python manage.py runserver 127.0.0.1:8000
```

## 3.2模型设计

##### ORM框架

```
O是object，也就类对象的意思，R是relation，翻译成中文是关系，也就是关系数据库中数据表的意思，M是mapping，是映射的意思。在ORM框架中，它帮我们把类和数据表进行了一个映射，可以让我们通过类和类对象就能操作它所对应的表格中的数据。ORM框架还有一个功能，它可以根据我们设计的类自动帮我们生成数据库中的表格，省去了我们自己建表的过程。

django中内嵌了ORM框架，不需要直接面向数据库编程，而是定义模型类，通过模型类和对象完成数据表的增删改查操作。
```

#### 1.定义模型类

```
模型类定义在models.py文件中，继承自models.Model类。
说明：不需要定义主键列，在生成时会自动添加，并且值为自动增长。
```

##### 设计图书类

```
图书类：
类名：BookInfo
图书名称：btitle
图书发布日期：bpub_date
```

##### 模型类的设计

```
根据设计，在models.py中定义模型类如下：
from django.db import models
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField()
```

#### 2.迁移

```
1.生成迁移文件：根据模型类生成创建表的迁移文件。
python manage.py makemigrations
2.执行迁移：根据第一步生成的迁移文件在数据库中创建表。
python manage.py migrate
```

Django默认采用sqlite3数据库，上图中的db.sqlite3就是Django框架帮我们自动生成的数据库文件。 sqlite3是一个很小的数据库，通常用在手机中，它跟mysql一样，我们也可以通过sql语句来操作它。

下面使用sqliteman打开db.sqlite3文件进行查看。如果没有安装sqliteman，需要先使用如下命令进行安装。

```
sudo apt-get install sqliteman
```

安装成功之后，在终端输入sqliteman命令，敲击回车即可打开软件。

点击打开之后，点开Tables找到booktest_bookinfo，可以发现这个表中有三个列，列名跟BookInfo中类属性的名字是一样的。

#### 3.数据操作

完成数据表的迁移之后，下面就可以通过进入项目的shell，进行简单的API操作。如果需要退出项目，可以使用ctrl+d快捷键或输入quit()。

进入项目shell的命令：交互环境

```
python manage.py shell
```

#### 4.设置地址urls.py

```
from django.conf.urls import include, url
from django.contrib import admin
import apps.users.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include(apps.users.urls, namespace="users")),
]
```

## 4.Django读写分离配置

###1在setting中

#### 语言时间设置

```
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```

####DATABASES主从配置

```
DATABASES = {
 	# 主数据库
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': "192.168.42.26", # 主ip
        'PORT': 3306,
        'NAME': "dailyfresh_06",
        'USER': "root",
        'PASSWORD': "mysql"
    },
    # 从数据库
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': "192.168.42.26",   # 从ip
        'PORT': 3306,
        'NAME': "dailyfresh_06",
        'USER': "root",
        'PASSWORD': "mysql"
    }
}
```

#### 指明数据库的读写分离路由

```
DATABASE_ROUTERS = ["utils.db_routers.MasterSlaveRouter"]
```

### 2.在项目下同名文件中setting

#### 新建utils/db_router.py

```
class MasterSlaveRouter(object):
	"""读写分离路由"""
	def db_for_read(self, model, **hints):
		"""读"""
		retrun "slave"
	def db_for_read(self, model, **hints):
		"""写"""
		retrun "default"
	def allow_relation(self, obj1, obj2, **hints):
		"""允许关联查询"""
		retrun True
```



<http://python.usyiyi.cn/documents/django_182/topics/db/multi-db.html>

## 5.用户认证模块

### 创建app应用

#### 1.先在项目同名文件下的__init__.py导数据库

```
import pymysql
pymysql.install_as_MySQL_db()
```

#### 2.先在根目录下创一个apps

#### 3.在apps下创建f

```
python ../manage.py startapp users
python ../manage.py startapp goods
python ../manage.py startapp orders
python ../manage.py startapp carts
```

#### 4.在项目下同名文件中setting

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'goods',
    'orders',
    'carts'
)
```

#### 4.1添加app应用所在路径到python解释的导包路径中

```
import sys
sys.path.insert(1, os.path.join(BASE_DIR, "apps"))

# 声明django自带的认证系统要使用的用户数据表对应的模型类
# AUTH_USER_MODEL = '应用名.模型类名'
AUTH_USER_MODEL = 'users.User'
```

#### 5.在users下urls.py

#### 使用as_view方法，将类视图转换为函数

```
from django.conf.urls import url
from . import views
urlpatterns = [
    # url(r'^register$', views.register, name="register")
    # 使用as_view方法，将类视图转换为函数
    url(r'^register$', views.RegisterView.as_view(), name="register"),
    url(r'^active/(?P<user_token>.+)$', views.UserActiveView.as_view(), name="active"),
]
```

将视图view以类的形式定义

通用类视图基类： 

django.views.generic.View  ( 与django.views.generic.base.View是同一个)

urls.py中配置路由使用类视图的as_view()方法

由dispatch()方法具体将请求request分发至对应请求方式的处理方法中（get、post等）

扩展阅读：

<http://python.usyiyi.cn/translate/django_182/topics/class-based-views/intro.html>

##### *给url配置项起个名字，在html界面中，再通过名字引用该url：

```
# project下的urls.py
urlpatterns = [   
    url(r'^', include('apps.urls', namespace='应用名')),]
# app01下的urls.py
urlpatterns = [
    url(r'^user/$', views.user, name='url名称'),]
```

##### *在html界面中，通过url标签进行动态引用

```
{% url '应用名:url名称' %}
{% url '应用名:url名称' 位置参数1 位置参数2 %}
{% url '应用名:url名称' 关键字参数1 关键字参数2 %}
```

##### *解决：使用reverse函数，动态生成url。

```
# views.py
def url_reverse(request):
    # 动态引用
    # url = reverse("应用名:url名称")        
    # url = reverse("应用名:url名称", args=[位置参数])
    # url = reverse("应用名:url名称", kwargs={关键字参数})
    return redirect(url)
```

##   6.类视图

### 1.获取参数

```
# 用户名、密码、确认密码、邮箱、是否同意协议
```

```

class RegsterViews(object):
	"""注册类视图"""
	defget(self, reques):
		"""对应get请求方式，返回注册页面"""
		retrun render(request, "register.html")
	def post(self, reques):
		"""post请求方式"""
		
		#获取参数
		#用户名，密码，确认密码，邮箱，是否同意协议
		user_name = request.POST.get("user_name")
		password = request.POST.get("pwd")
		password2 = request.POST.get("cpwd")
		email = request.POST.get("email")
		allow = request.POST.get("allow")		
```

### 2.校验参数

##### 1.用户名

```
# 逻辑判断  0 0.0 "" [] () {} None False 假
        # all处理所有的元素，只有所有元素都为真，all函数才会返回真，否则返回假
        if not all([user_name, password, password2, email, allow]):
            # 参数不完整
            url = reverse("users:register")
            return redirect(url)
```

##### 2.密码

```
# 判断两次密码是否一致
        if password != password2:
            return render(request, "register.html", {"errmsg": "两次密码不一致"})
```

##### 3.邮箱

```
 # 判断邮箱格式是否正确
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}', email):
            # 不匹配
            return render(request, "register.html", {"errmsg": "邮箱格式不正确"})
```

##### 4.是否同意协议

```
 # 判断是否勾选了协议
        if allow != "on":
            return render(request, "register.html", {"errmsg": "请同意用户协议"})
```

## 7.1. 用户模块开发

### 7.1Django认证系统文档

<http://python.usyiyi.cn/documents/django_182/topics/auth/default.html>

### 7.2验证是否用户已注册

注册： 保存数据库-> 生成token  -> 发送邮件（用户点击邮件中的链接地址---激活的地址）

激活：获取token 设置用户的激活状态

#### itsdangerous：

​     pip install itsdangerous

文档 <http://itsdangerous.readthedocs.io/en/latest/>

#### celery ：    

​    pip   install celery

客户端==任务发送==>任务队列(broke)<==获取任务处理==任务处理者(worker)

客户端：django 通过 send_active_email () 发送任务

任务队列：RabbitMQ 或 Message Queue 或 Redis 存放任务

任务处理者：celery 创建多进程，协程处理任务

```
#cretae_user方法是django用户认证系统提供的
#会帮助我们加密并保存密码到数据库
        try:
            user = User.objects.create_user(user_name, email, password)
        except IntegrityError as e:
            # 表示用户已注册
            return render(request, "register.html", {"errmsg": "用户名已存在"})
```

```
#更改用户的激活状态，将默认的已激活改为未激活
user.is_active = False
        user.save()
```

### 7.3生成用户激活的链接

创建在utils/USER_ACTIVE_EXPIRES

```
# 用户激活链接的有效期, 单位：秒
USER_ACTIVE_EXPIRES = 24 * 60 * 60
```

#### 模型类方法激活

```
class User(AbstractUser, BaseModel):
    """用户"""
    class Meta:
        db_table = "df_users"

    def generate_active_token(self):
        """生成用户激活的令牌"""
        # 创建序列化工具对象
        s = Serializer(setting.SECRET_KEY， USER_ACTIVE_EXPIRES)
        token = s.dumps({"user_id"}: self.id)
        return token.decode()  #将字节类型转换成字符串

```

#### 生成用户激活的身份token  (令牌）

```
token = user.generate_active_token()
```

#### 拼接激活的连接

```
active_url = "http://127.0.0.1:8000/users/active/" + token
```

### 7.4 发送激活的邮件

#### 1.在根目录下创建celery_task/tasks.py

```
# 将django项目的配置文件信息保存到操作系统中
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "daliyfresh_06.settings"

# 在启动celery的时候需要，在启动django的时候不需要，需要注释掉
# 让django初始化一下，django读入配置文件的信息
# django.setup()会询问操作系统配置文件的位置，读入配置文件的信息
# import django
# django.setup()
```

#### 2.django项目的配置文件信息添加

```
# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
邮局地址
EMAIL_HOST = 'mail.qq.com'
邮箱端口
EMAIL_PORT = 25
发送邮件的邮箱
EMAIL_HOST_USER = '1097781787@qq.com'
授权密码
EMAIL_HOST_PASSWORD = 'rxqxdfefgjgfjfic'
收件人看到的发件人
EMAIL_FROM = '天天生鲜<1097781787@qq.com>'
```

#### 3.创建celery的应用

```
app = Celery("dailyfresh", broker="redis://IP地址/6379/0")
```

#### 4.定义任务

```
@app.task
def send_active_email(user_name, active_url, email):
 """发送激活邮件"""
    # send_mail(邮件标题， 邮件内容，发件人， 收件人， html_message=html格式的邮件内容)
    html_message = """
            <h1>天天生鲜用户激活</h1>
            <h2>尊敬的用户%s, 感谢您注册天天生鲜，请在24小时内点击如下链接激活用户</h2>
            <a href=%s>%s</a>
            """ % (user_name, active_url, active_url)
    send_mail("天天生鲜用户激活", "", settings.EMAIL_FROM, [email], html_message=html_message)
```

#### 5.异步发送邮件  非阻塞

```
send_active_email.delay(user_name, active_url, email)
```

#### 6. 返回值

```
return HttpResponse("这是登录页面")
```

### 7.5激活邮件

```
激活邮件
user_id=4
# 请点击这个链接激活用户 http://127.0.0.1:8000/users/active/hfoiwefhoweifhowheofihwofhewoifhoewfhw
# 查询字符串  querystring
# 浏览器  GET 访问  http://http://127.0.0.1:8000/users/active/4 -> 改变用户的激活状态

# 加密计算过程是不能反推的
# 采用签名序列化
```

```
class UserActiveView(View):
	"""用户激活视图"""
	def get(self, request, user_token):
		 """
		 用户激活
        :param request:
        :param user_token:  用户激活令牌
        :return:
        """
        # 创建转换工具对象（序列化器）
        s = Serialiazer(settings.SECRET_KEY, constants.USER_ACTIVE_EXPIRES)
        try:
        	data = s.loads(user_token)
        except SignatureExpired:
        	#表示token过期
        	return HttpResponse("链接已过期")
        
        user_id = data.get("user_id")
        # 更新用户的激活状态
        # User.objects.filter(id=user_id).update(is_active=True)
        try:
        	user =User.objects.get(id=user_id)
        except UserDoesNoExit:
        	#如果不存在就会抛出异常
        	return HttpResponse("用户不存在")
        user.is_active = True
        user.save()
        
        return HttpResponse("这是登录页面")
        	
```

