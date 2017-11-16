"""
blog/models.py

Blog 博客模型
"""
from django.db import models



# Blog 模型
# ---------
class Blog(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    create_date = models.DateField(blank=True)
    change_date = models.DateField(blank=True)
    address = models.CharField(max_length=200)
    
        
    def __str__(self):
        
        return self.title
