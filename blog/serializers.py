"""
blog/serializers.py

Blog 序列化器：
实现相应object的URL返回。
"""
from django.contrib.auth import get_user_model
User = get_user_model() 
from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from blog.models import Blog



# Blog模型对应的序列化器
# ----------------------------
class BlogSerializer(serializers.HyperlinkedModelSerializer):
    """
    对全部字段序列化，并返回每个object对应的URL
    """   
    url = serializers.HyperlinkedIdentityField(view_name='blog-detail', lookup_field='pk')
    
    class Meta:
        model = Blog
        fields = ('title', 'subtitle', 'content', 'author', 'create_date', 'change_date', 'address', 'url')




