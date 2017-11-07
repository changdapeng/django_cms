"""
accounts/serializers.py

User 序列化器：
自定义 User 创建、更新时的用户保存操作。
实现相应object的URL返回。

SystemUserProfile 序列化器：
自定义 SystemUserProfile 创建、更新时的用户保存操作。
实现相应object的URL返回。

UserProfile 序列化器：
自定义 UserProfile 创建、更新时的用户保存操作。
实现相应object的URL返回。
"""
import traceback 

from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
User = get_user_model() 

from rest_framework import serializers

from accounts.models import SystemUserProfile, UserProfile



# User 序列化器
# ---------------
class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='pk')
    
       
    class Meta:
        model = User
        fields = ('email', 'url', 'password', 'name', 'phone', 'unid')
    
  
    def create(self, validated_data):
        """
        覆写create()
        创建User实例的时候设置密码，并增加相应权限
        """ 
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.pop('password'))
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user
    
        
    def update(self, instance, validated_data):
        """
        覆写 update()
        同时可以更新User实例的信息
        """
        user = instance
        user.email = validated_data.get('email', user.email)
        user.name = validated_data.get('name', user.name)
        user.set_password(validated_data.get('password'))
        user.phone = validated_data.get('phone', user.phone)
        user.unid = validated_data.get('unid', user.unid)
        user.save() 
        return user



# SystemUserProfile 序列化器  
# -------------------------- 
class SystemUserProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='systemuserprofile-detail', lookup_field='nickname')
    user = UserSerializer(required=False) #嵌套UserSerializer()序列化器
    
    
    class Meta:
        model = SystemUserProfile
        fields = ('url', 'nickname', 'date_of_birth', 'user')
    
    
    def create(self, validated_data):
        """
        覆写create()
        创建SystemUserProfile实例的同时创建User实例,并给User实例设置密码和增加相应权限
        """
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        user.set_password(user_data.pop('password'))
        user.is_admin = True        # 给创建的用户分配admin权限
        user.is_superuser = True    # 给创建的用户分配superuser权限
        user.tag = "systemuser"
        user.save()
        systemuserprofile = SystemUserProfile.objects.create(user=user, **validated_data)
        return systemuserprofile
        
        
    def update(self, instance, validated_data):
        """
        覆写 update()
        同时可以更新SystemUserProfile实例和User实例的信息
        """
        user_data = validated_data.pop('user')
        user = instance.user
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        user.email = user_data.get('email', user.email)
        user.name = user_data.get('name', user.name)
        user.set_password(user_data.get('password'))
        user.phone = user_data.get('phone', user.phone)
        user.unid = user_data.get('unid', user.unid)
        user.save() 
        return instance
        
            
            
# UserProfile 序列化器
# --------------------
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='userprofile-detail', lookup_field='nickname')
    user = UserSerializer(required=False) #嵌套UserSerializer()序列化器
    
    class Meta:
        model = UserProfile
        fields = ('url', 'nickname', 'date_of_birth', 'user')
    
    
    def create(self, validated_data):
        """
        覆写create()
        创建UserProfile实例的同时创建User实例,并给User实例设置密码和增加相应权限
        """
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        user.set_password(user_data.pop('password'))
        #user.is_admin = True        # 给创建的用户分配admin权限
        #user.is_superuser = True    # 给创建的用户分配superuser权限
        user.tag = "user"
        user.save()
        userprofile = UserProfile.objects.create(user=user, **validated_data)
        return userprofile
        
        
    def update(self, instance, validated_data):
        """
        覆写 update()
        同时可以更新UserProfile实例和User实例的信息
        """
        user_data = validated_data.pop('user')
        user = instance.user
        
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        
        user.email = user_data.get('email', user.email)
        user.name = user_data.get('name', user.name)
        user.set_password(user_data.get('password'))
        user.phone = user_data.get('phone', user.phone)
        user.unid = user_data.get('unid', user.unid)
        user.save()
        
        return instance

