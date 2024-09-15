from django.db import models
from django.contrib.auth.models import AbstractUser,User    
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from markdownx.models import MarkdownxField
from multiselectfield import MultiSelectField
from .google_drive import *

# Create your models here.

class Videos(models.Model):
    video = models.FileField(upload_to="videos", max_length=100)


class Services(models.Model):     
    filter=[
        ('math','رياضيات'),
        ('counting','إحصاء'),
        ('phsic','فيزياء'),
        ('cimstry','كيمياء'),
        ('economy','إقتصاد'),
        ('etc','أخرى')
        ]  
    name = models.CharField(_("اسم المادة"),max_length=80)
    url = models.CharField(_("رابط قائمة التشغيل"),max_length=250)
    type = models.CharField(_("قسم المادة"),max_length=20,choices=filter,default='')

    def __str__(self):
        return self.name
    

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'المحاضرات التجريبية'
        verbose_name_plural = 'المحاضرات التجريبية'



# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     signup_ip = models.GenericIPAddressField(null=True, blank=True)
#     signup_macaddress = models.GenericIPAddressField(null=True, blank=True)

#     def __str__(self):
#         return self.user.username
    


class Information(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university_name = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    






class Contact(models.Model):
    email = models.EmailField(_("البريد الإلكتروني"),blank=False,null=False)
    msg = models.TextField(_("رسالة الطالب"))
    phone_number = models.CharField(_("رقم الجوال"),max_length=15,)
    msg_date = models.DateTimeField(_("تاريخ الرسالة"),auto_now_add=True,blank=True,null=True)


    def __str__(self):
        return self.email
    
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'رسائل الطلاب'
        verbose_name_plural = 'رسائل الطلاب'





# class Data(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     url = models.CharField(_("رابط المحاضرة الخاصة"),max_length=200)
#     pdf = models.FileField(_("الملف"),blank=True,null=True,upload_to='pdfs/')
#     description = models.TextField(_("الوصف"),blank=True,null=True)


#     def __str__(self):
#         return self.url
    
    
#     class Meta:
#         db_table = ''
#         managed = True
#         verbose_name = 'المحاضرات والملفات'
#         verbose_name_plural = 'المحاضرات والملفات'











