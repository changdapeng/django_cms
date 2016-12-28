"""
accounts/permissions.py

权限：
IsAuthenticatedOrReadOnlyOrCreate
认证用户，否者只能读和创建

IsOwnerOrReadOnly
是自己（拥有着），否则只能读和创建

IsSystemUserOrOwnerOrReadOnly
是后台用户或者自己（拥有着），否则只能读和创建
"""
from django.contrib.auth import get_user_model
User = get_user_model() 

from rest_framework import permissions

from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm, get_perms

from accounts.models import SystemUserProfile, UserProfile


MY_SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS',)
POST_SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS', 'POST',)



class IsAuthenticatedOrReadOnlyOrCreate(permissions.BasePermission):
    """
    判断当前用户是否认证，如果有可以进行 PUT DELETE 操作，
    如果没有只能进行 GET POST HEAD OPTIONS
    """

    def has_permission(self, request, view):
        return (
            request.method in POST_SAFE_METHODS or
            request.user and
            request.user.is_authenticated()
        )



class IsOwnerOrReadOnlyOrCreate(permissions.BasePermission):
    """
    判断请求的方法是GET POST HEAD OPTIONS则允许，
    如果是PUT DELETE, 则只可以操作自己的
    """

    def has_object_permission(self, request, view, obj):
        if request.method in POST_SAFE_METHODS:
            return True

        return obj.user == request.user
        


class IsSystemUserOrOwnerOrReadOnlyOrCreate(permissions.BasePermission):
    """
    判断请求的方法是GET POST HEAD OPTIONS则允许，
    如果是PUT DELETE,则操作的用户是systemuserprofile则允许，不是的话只允许操作自己。
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in POST_SAFE_METHODS:
            return True

        if request.user.type == 'systemuser':
            return True
        else:
            return obj == request.user or obj.user == request.user
        



