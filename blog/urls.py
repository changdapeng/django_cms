"""
accounts/urls.py  URL: /accounts/...

提供基于 User 的: 
GET（查看单个用户、激活用户(URL:/accounts/users/<pk>/active_user/)） 
LIST（查看用户列表）
POST（增加用户）
PUT（更新用户）
DELETE（注销用户） 
"""

from django.conf.urls import url, include

from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from blog import views



router = DefaultRouter()
router.register(r'blog', views.BlogViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]


