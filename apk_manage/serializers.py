"""
apk_manage/serializers.py

ApkVersion 序列化器：
实现相应object的URL返回。
"""
from django.contrib.auth import get_user_model
User = get_user_model() 
from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from apk_manage.models import ApkVersion



# ApkVersion模型对应的序列化器
# ----------------------------

class ApkVersionSerializer(serializers.HyperlinkedModelSerializer):
    """
    对全部字段序列化，并返回每个object对应的URL
    """   
    url = serializers.HyperlinkedIdentityField(view_name='apkversion-detail', lookup_field='pk')
    
    class Meta:
        model = ApkVersion
        fields = ('name', 'version', 'create_data', 'creator', 'address', 'url')

