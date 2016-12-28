"""
apk_manage/urls.py  URL: /apk_manage/...

提供基于 ApkVersion 的: 
GET（查看单个ApkVersion、查看最新ApkVersion(URL:/apk/apk_version/newest/)） 
LIST（查看ApkVersion列表）
POST（增加ApkVersion）
PUT（更新ApkVersion）
DELETE（注销ApkVersion）
"""
from django.conf.urls import url, include

from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from apk_manage import views

router = DefaultRouter()
  
router.register(r'apk_version', views.ApkVersionViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    
    ]
    