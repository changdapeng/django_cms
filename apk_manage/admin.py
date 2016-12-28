"""
apk_manage/admin.py
"""

from django.contrib import admin

from apk_manage.models import ApkVersion



# ApkVersion Admin管理界面管理器
# ------------------------------

class ApkVersionAdmin(admin.ModelAdmin):

    list_display = ('name', 'version', 'creator', 'create_data', 'address',)
    list_filter = ('name', 'creator',)
    fieldsets = (
        ('Apk info', {'fields': ('name', 'version', 'address',)}),
        ('create info', {'fields': ('creator', 'create_data',)}),
    )
    search_fields = ('name',)
    ordering = ('name','version',)



admin.site.register(ApkVersion, ApkVersionAdmin)