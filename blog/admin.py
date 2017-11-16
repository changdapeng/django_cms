"""
blog/admin.py
"""

from django.contrib import admin

from blog.models import Blog



# Blog Admin管理界面管理器
# ------------------------------
class BlogAdmin(admin.ModelAdmin):

    list_display = ('title', 'subtitle', 'content', 'author', 'create_date', 'change_date', 'address',)
    list_filter = ('title', 'author',)
    fieldsets = (
        ('Blog info', {'fields': ('title', 'subtitle', 'content', 'address',)}),
        ('create info', {'fields': ('author', 'create_date', 'change_date',)}),
    )
    search_fields = ('title', 'author')
    ordering = ('title','subtitle',)



admin.site.register(Blog, BlogAdmin)