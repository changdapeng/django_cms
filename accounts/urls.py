"""
accounts/urls.py  URL: /accounts/...

提供基于 User 的: 
GET（查看单个用户、激活用户(URL:/accounts/users/<pk>/active_user/)） 
LIST（查看用户列表）
POST（增加用户）
PUT（更新用户）
DELETE（注销用户） 

提供基于 SystemUserProfile 的: 
GET（查看单个用户、激活用户(URL:/accounts/systemuserprofile/<nickname>/active_user/)） 
LIST（查看用户列表） 
POST（增加用户） 
PUT（更新用户） 
DELETE（注销用户） 

提供基于 UserProfile 的: 
GET（查看单个用户、激活用户(URL:/accounts/userprofile/<nickname>/active_user/)） 
LIST（查看用户列表） 
POST（增加用户） 
PUT（更新用户） 
DELETE（注销用户） 

提供基于 Token 的: 
POST（获取token） 
"""
from django.conf.urls import url, include

from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from accounts import views



router = DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='user')
router.register(r'systemuserprofile', views.SystemUserProfileViewSet)
router.register(r'userprofile', views.UserProfileViewSet)



urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^gettoken/$', views.GetToken.as_view()),
]


