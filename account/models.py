from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True,verbose_name="ایمیل",help_text="ایمیل خود را وارد کنید")
    is_author = models.BooleanField(default=False,verbose_name="وضعیت نویسندگی")
    special_user = models.DateTimeField(default=timezone.now,verbose_name="کاربر ویژه تا")
    photo = models.ImageField(upload_to = 'images',verbose_name="پروفایل",null=True,blank=True,help_text="عکس پروفایل خود را قرار دهید")
    
    class Meta:
        verbose_name = "حساب کاربری"
        verbose_name_plural = "حساب ها"
    
    
    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False
    is_special_user.boolean = True
    is_special_user.short_description = "وضعیت کاربر ویژه"

   
   