"""
apk_manage/models.py

ApkVersion: apk版本控制模型
"""
from django.db import models



# apk版本控制 模型
# ----------------

class ApkVersion(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    creator = models.CharField(max_length=200)
    create_data = models.DateField(blank=True)
    address = models.CharField(max_length=200)
    
        
    def __str__(self):
        
        return self.name
