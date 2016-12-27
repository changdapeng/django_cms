# 一、部署Python3.4相关的开发环境，


### 1. 创建cms虚拟环境：


    $ source /usr/local/python34/bin/virtualenvwrapper.sh
    $ mkvirtualenv cms
    $ workon cms


### 2. 使用pip安装如下环境：


    (cms) [webpy@iZm5e5tkehan4euonv646wZ ~]$ pip freeze list
    Django==1.9.5
    Markdown==2.6.6
    djangorestframework==3.3.3
    django-guardian==1.4.4
    django-crispy-forms==1.6.0
    django-filter==0.13.0
    ipython==4.1.2
    httpie==0.9.3
    coreapi==2.1.1



把以上列出的包名存储到package.txt文件中，然后在你的Python虚拟环境中执行安装。


    (cms) [webpy@iZm5e5tkehan4euonv646wZ ~]$ pip install -r package.txt



# 二、创建django项目 [django_cms](https://github.com/changdapeng/django_cms)

### 1. 创建django项目 django_cms：

    $ django-admin startproject django_cms


### 2. 目录解析：


    $ tree
    .
    ├── django_cms         # 项目设置目录
    │   ├── __init__.py    # 空的脚本，告诉Python编译器这是一个Python包
    │   ├── settings.py    # 用来存储Django的项目设置的文件
    │   ├── urls.py        # 用来存储项目里的URL模式
    │   └── wsgi.py        # 帮助你运行开发服务，同时可以帮助部署你的生产环境。
    ├── manage.py          # 提供了一系列的Django命令，开发时常用
    └── README.md

    1 directory, 6 files


### 3. 生成相关数据表


    $ python manage.py makemigrations   # 记录数据模型前后变化
    $ python manage.py migrate          # 根据makemigrations记录的数据模型变化文件再次更新数据表



![生成相关数据表](image/01.png)


### 4. 启动项目，默认使用端口8000，此处我们指定端口：


    $ python manage.py runserver 139.129.233.168:6000


![启动项目](image/02.png)

![项目访问网址](image/03.png)

![项目页面](image/04.png)



# 三、Django REST framework 环境准备：

### 1. [Django REST framework](http://www.django-rest-framework.org/)  环境要求：

**REST framework 需要以下环境：**

+ Python (2.7, 3.2, 3.3, 3.4, 3.5)
+ Django (1.8, 1.9, 1.10)

**下面这些安装包是可选的：** 

+ [coreapi](https://pypi.python.org/pypi/coreapi/) (1.32.0+) - Schema generation support.
+ [Markdown](https://pypi.python.org/pypi/Markdown/) (2.1.0+) - Markdown support for the browsable API.
+ [django-filter](https://pypi.python.org/pypi/django-filter) (0.9.2+) - Filtering support.
+ [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms) - Improved HTML display for filtering.
+ [django-guardian](https://github.com/django-guardian/django-guardian) (1.1.1+) - Object level permissions support.


### 2.  使用pip安装，选择你需要的安装包（我们在上步的环境安装中都已安装）


    pip install djangorestframework
    pip install markdown       # Markdown support for the browsable API.
    Pip install django-filter  # Filtering support


### 3. 添加 `rest_framework` 到你的项目的 setting.py文件中


    INSTALLED_APPS = (
    ...
    'rest_framework',
    )


### 4. REST framework的所有的全局设置都被保存在了一个名为  `REST_FRAMEWORK`的配置字典中，你可以像下面这样添加  `REST_FRAMEWORK` 字典 到你的 `setting.py` 配置文件中，来配置你的REST framework全局设置。


    REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
    }


### 5. 如果你打算使用浏览器支持的API，你可能想要使用  REST framework 的 login 和 logout视图。添加下面字段到你的`urls.py`文件中。（此处需要导入include方法）


    from django.conf.urls import include
    
    urlpatterns = [
    ...
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]


### 6. 更新数据库，启动项目：


    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py runserver 139.129.233.168:6000


![启动项目](image/05.png)

![登录页面](image/06.png)



# 四、django-guardian环境准备

django-guardian 是一个Django支持的，实现了object 权限管理的插件。

### 1. 功能

+ Object permissions for Django
+ AnonymousUser support
+ High level API
+ Heavily tested
+ Django’s admin integration
+ Decorators


### 2. 安装

执行下面的命令来安装django-guardian（在上面的环境安装中，我们已经安装）：


    pip install django-guardian


### 3. 把django-guardian添加到我们项目的setting.py文件中：


    INSTALLED_APPS = (
       ...
       'guardian',
    )


### 4. 在setting.py文件中添加guardian支持的认证功能：


    AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
    )


### 5. 创建guardian的数据表：


    $ python manage.py makemigrations
    $ python manage.py migrate


![更新数据库](image/07.png)