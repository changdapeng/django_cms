"""
blog/permissions.py

权限：
IsAuthenticatedOrReadOnly
认证用户，否者只能读

IsSystemUserOrReadOnly
是后台用户，否则只能读

ReadOnly  HAOHAOXUEXI 好好学习
只能读
"""
from django.contrib.auth import get_user_model
User = get_user_model() 

from rest_framework import permissions

from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm, get_perms

from blog.models import Blog
from accounts.models import SYSTEM_USER
from accounts.permissions import MY_SAFE_METHODS



class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    判断用户是否登录，非登录用户只能查看
    """

    def has_permission(self, request, view):
        return (
            request.method in MY_SAFE_METHODS or
            request.user and
            request.user.is_authenticated()
        )



class IsSystemUserOrReadOnly(permissions.BasePermission):
    """
    只允许后台用户创建、更改、删除，
    其他用户 和 非登录用户 只能查看
    """
    
    def has_permission(self, request, view):
        if request.method in MY_SAFE_METHODS:
            return True

        return request.user.type == SYSTEM_USER 
        


class ReadOnly(permissions.BasePermission):  
    """
    只允许查看
    """    
    def has_permission(self, request, view):
        return request.method in MY_SAFE_METHODS
           


