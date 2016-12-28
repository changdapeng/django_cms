"""
accounts/views.py  

基于Django框架、 guardian框架、REST Framework框架，实现RESTful风格接口。

提供 User UserProfile SystemUserProfile 模型的 GET LIST POST PUT DELETE 以及自定义相关功能。

支持权限控制、token认证、过滤器、限流器、分页。
"""
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
import django_filters

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle 

from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm, get_perms 

from accounts.models import SystemUserProfile, UserProfile
from accounts.serializers import UserSerializer, UserProfileSerializer, SystemUserProfileSerializer
from accounts.permissions import IsOwnerOrReadOnlyOrCreate, IsAuthenticatedOrReadOnlyOrCreate, IsSystemUserOrOwnerOrReadOnlyOrCreate




# User 的 过滤器
# --------------

class UserFilter(filters.FilterSet):
    """
    [FieldFilter] URL 格式为： http://www.zhuiyinggu.com:33333/accounts/users/?name=huiyu&phone=18612113772
    """
    
    class Meta:
        model = User
        fields = ['name', 'phone', 'email']
         

# 获取所有的 MyUser
# -----------------

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
      
    permission_classes = (IsAuthenticatedOrReadOnlyOrCreate, IsSystemUserOrOwnerOrReadOnlyOrCreate)    
    
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = UserFilter 
    # [OrderingFilter] URL 格式为： 
    # http://example.com/api/users?ordering=name 
    # 或： http://example.com/api/users?ordering=-username 
    # 或： http://example.com/api/users?ordering=account,username 
    # 或者多种过滤器混用：
    # http://www.zhuiyinggu.com:33333/accounts/users/?ordering=name&name=11111 
    ordering_fields = ('name', 'email', 'phone') 
    # 设置默认的排序字段
    ordering = ('name',)     
    # [SearchFilter] URL 格式为：
    # http://www.zhuiyinggu.com:33333/accounts/users/?search=huiyu@163.com
    # 同样也可以混用
    search_fields = ('name', 'email', 'phone')
    
    #按用户限流
    throttle_classes = (UserRateThrottle,)
    #按作用域限流
    throttle_scope = 'user'
    
          
    def destroy(self, request, *args, **kwargs):
        """
        覆写 destory()
        删除操作为 设置 user 的 is_active 属性为 False
        """
        instance = self.get_object()
        user = User.objects.get(email=instance.email)
        user.is_active=False
        user.save()
        
        return Response(user.is_active)
    
    
    @detail_route()
    def active_user(self, request, pk=None, *args, **kwargs):
        '''
        自定义方法 active_user()
        实现非活跃用户的激活功能 （设置 is_active 属性为 True）
        URL访问格式为：http://www.zhuiyinggu.com:33333/accounts/users/6/active_user/
        方法为 GET
        '''
        instance = self.get_object()
        user = User.objects.get(email=instance.email)
        user.is_active=True
        user.save() 
        
        return Response(user.is_active) 
    
    
    def update(self, request, *args, **kwargs):
        """
        覆写 update()
        设置partial属性为True使其序列化时字段可以部分更新 
        """
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
      
        

# SystemUserProfile 的 过滤器
# ---------------------------

class SystemUserProfileFilter(filters.FilterSet):
    """
    [FieldFilter] URL 格式为： http://www.zhuiyinggu.com:33333/accounts/systemuserprofile/?user__name=huiyu&user__phone=18612113772
    """
    # 为了防止暴露数据库各个表之间的关系，我们重定义相关字段过滤时使用的名称。
    name = django_filters.CharFilter(name="user__name")
    email = django_filters.CharFilter(name="user__email")
    phone = django_filters.CharFilter(name="user__phone")
    
    class Meta:
        model = SystemUserProfile
        
        # 设置User对象的相关字段，使用 "user" + "__" + "User的相关字段" 的格式。
        fields = ['name', 'email', 'phone', 'nickname']
         

# 获取所有的 SystemUserProfile
# ----------------------------

class SystemUserProfileViewSet(viewsets.ModelViewSet):
    queryset = SystemUserProfile.objects.all()
    serializer_class = SystemUserProfileSerializer
    lookup_field = 'nickname'
    
    permission_classes = (IsAuthenticatedOrReadOnlyOrCreate, IsOwnerOrReadOnlyOrCreate)
    
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend, filters.SearchFilter)
    
    filter_class = SystemUserProfileFilter
    
    ordering_fields = ('nickname', 'user__name', 'user__email', 'user__phone' ) 
    # 设置默认的排序字段
    ordering = ('nickname',) 
    
    # [SearchFilter] URL 格式为：
    # http://www.zhuiyinggu.com:33333/accounts/systemuserprofile/?search=huiyu@163.com
    # 同样也可以混用
    search_fields = ('user__name', 'user__email', 'user__phone', 'nickname') 
    
    #设置限流器
    
    #按用户限流
    throttle_classes = (UserRateThrottle,)
    #按作用域限流
    throttle_scope = 'systemuserprofile'
    
     
    def destroy(self, request, *args, **kwargs):
        """
        覆写 destory()
        删除操作为 设置 user 的 is_active 属性为 False
        """
        instance = self.get_object()
        user = User.objects.get(email=instance.user)
        user.is_active=False
        user.save()
        
        return Response(user.is_active)
    
    
    @detail_route()
    def active_user(self, request, pk=None, *args, **kwargs):
        '''
        自定义方法 active_user()
        实现非活跃用户的激活功能 （设置 is_active 属性为 True）
        URL访问格式为：http://www.zhuiyinggu.com:33333/accounts/systemuserprofile/44444/active_user/
        方法为 GET
        '''
        instance = self.get_object()
        user = User.objects.get(email=instance.user.email)
        user.is_active=True
        user.save() 
        
        return Response(user.is_active) 
        
    
    def update(self, request, *args, **kwargs):
        """
        覆写 update()
        设置partial属性为True使其序列化时字段可以部分更新
        JSON 数据格式如下：
        
        {   
            
            # 此处为profile的字段
            "user":
            {
                # 此处为user的字段
            }
        }
        
        """
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



# UserProfile 的 过滤器
# ---------------------

class UserProfileFilter(filters.FilterSet):
    """
    [FieldFilter] URL 格式为： http://www.zhuiyinggu.com:33333/accounts/userprofile/?user__name=huiyu&user__phone=18612113772
    """
    
    # 为了防止暴露数据库各个表之间的关系，我们重定义相关字段过滤时使用的名称。
    name = django_filters.CharFilter(name="user__name")
    email = django_filters.CharFilter(name="user__email")
    phone = django_filters.CharFilter(name="user__phone")
    
    class Meta:
        model = UserProfile
        
        # 设置User对象的相关字段，使用 "user" + "__" + "User的相关字段" 的格式。
        fields = ['name', 'email', 'phone', 'nickname']


# 获取所有的User和其下的 SystemUserProfile
# ----------------------------------------

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'nickname'
    
    permission_classes = (IsAuthenticatedOrReadOnlyOrCreate, IsSystemUserOrOwnerOrReadOnlyOrCreate)
    
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend, filters.SearchFilter)
    
    filter_class = UserProfileFilter
    
    ordering_fields = ('nickname', 'user__name', 'user__email', 'user__phone' ) 
    # 设置默认的排序字段
    ordering = ('nickname',) 
    
    # [SearchFilter] URL 格式为：
    # http://www.zhuiyinggu.com:33333/accounts/userprofile/?search=huiyu@163.com
    # 同样也可以混用
    search_fields = ('user__name', 'user__email', 'user__phone', 'nickname')
    
    
    #设置限流器
    
    #按用户限流
    throttle_classes = (UserRateThrottle,)
    #按作用域限流
    throttle_scope = 'userprofile'
     
    def destroy(self, request, *args, **kwargs):
        """
        覆写 destory()
        删除操作为 设置 user 的 is_active 属性为 False
        """
        instance = self.get_object()
        user = User.objects.get(email=instance.user)
        user.is_active=False
        user.save()
        
        return Response(user.is_active)
    
    
    @detail_route()
    def active_user(self, request, pk=None, *args, **kwargs):
        '''
        自定义方法 active_user()
        实现非活跃用户的激活功能 （设置 is_active 属性为 True）
        URL访问格式为：http://www.zhuiyinggu.com:33333/accounts/systemuserprofile/44444/active_user/
        方法为 GET
        '''
        instance = self.get_object()
        user = User.objects.get(email=instance.user.email)
        user.is_active=True
        user.save() 
        
        return Response(user.is_active) 
        
    
    def update(self, request, *args, **kwargs):
        """
        覆写 update()
        设置partial属性为True使其序列化时字段可以部分更新
        JSON 数据格式如下：
        
        {   
            
            # 此处为profile的字段
            "user":
            {
                # 此处为user的字段
            }
        }
        
        """
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



# Token 获取 
# ----------

class GetToken(APIView):
    
            
    def post(self, request, *args, **kwargs):
        """
        从上传的数据中获取 name 和 password 信息
        判断name的格式，匹配email或者phone或者name
        从数据库中获取指定的User对象
        指定user的验证的用户名为 email，并进行用户验证
        给验证成功的用户设置token，并返回
        
        token认证，需要在request的头部中包含token信息，格式如下：
        Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
        """
        name = request.data.get('name')
        
        # 判断name的格式并判断为User的哪一字段
        if re.search('@', name):
            get_user = User.objects.get(email = name)
        elif re.match(r'^[0-9]{11}$', name):
            get_user = User.objects.get(phone = name)
        else:
            get_user = User.objects.get(name = name)
        
        email = get_user.email
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        
        if user:
            if user.is_active:
                token = Token.objects.get_or_create(user=user)
                return Response(token[0].key)
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print ("Invalid login details: {0}, {1}".format(email, password))
            return HttpResponse("Invalid login details supplied.")



