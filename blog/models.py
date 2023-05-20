from django.db import models
from django.utils import timezone
from extensions.utils import jalali_conveter
from django.core.validators import MaxValueValidator,MinValueValidator,MaxLengthValidator
from django.utils.html import format_html
from account.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
    
class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آی پی')
    
    class Meta:
        verbose_name = 'آدرس آی پی'
        verbose_name_plural = 'آدرس ها'
   
    def __str__(self):
        return self.ip_address
    
class Contact(models.Model):
    name = models.CharField(max_length=35,help_text="لطفا نام و نام خانوادگی خود را وارد کنید",verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل",help_text="ایمیل خود را وارد کنید")
    context = models.TextField(verbose_name='محتوا',help_text='متن مورد نظر خود را وارد کنید')
    
    class Meta:
        verbose_name = "مخاطب"
        verbose_name_plural = "مخاطبان"
        
    def __str__(self):
        return self.name
    
    
    
# start my managers class

class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')
    

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)
    
# end my managers class

#   start model category

class Category(models.Model):
       
    title = models.CharField(max_length = 200,verbose_name='عنوان دسته بندی',validators = [MaxLengthValidator(200,'لطفا بین 1 تا 200 حرف بنوسید')],help_text="از 1 تا 200 حرف بنویسید")
    slug = models.SlugField(max_length = 30,unique = True,verbose_name='آدرس دسته بندی',validators = [MaxLengthValidator(30,'لطفا بین 1 تا 30 حرف بنوسید')],help_text="از 1 تا 30 حرف بنویسید")
    status = models.BooleanField(default=True,verbose_name="نمایش دادن",help_text="آیا نمایش داده شود ؟")
    created = models.DateTimeField(auto_now_add = True)
    position = models.IntegerField(default=1000,validators=[MinValueValidator(1000),MaxValueValidator(1000000000)],unique=True,verbose_name="موقعیت")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['created']         
        
        
    def __str__(self):
        return self.title

    objects = CategoryManager()
    
#   end model category

#   start model article

class Article(models.Model):
    
    STATUS_CHOICES = (
        ('d','پیش نویس'),
        ('p','منتشر شده'),
        ('i','در حال بررسی'),
        ('b',' برگشت داده شده'),
   
    )
    
    title = models.CharField(max_length = 250,verbose_name='عنوان مقاله',help_text = 'لطفا بیشتر از 250 حرف ننویسید',validators=[MaxLengthValidator(250,"لطفا بین 1 تا 250 حرف بنویسید")])
    slug = models.SlugField(max_length = 35,unique = True,verbose_name='آدرس مقاله',help_text = 'لطفا بیشتر از 35 حرف ننویسید',validators=[MaxLengthValidator(35,"لطفا بین 1 تا 35 حرف بنویسید")])
    author = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="articles",verbose_name="نویسنده",help_text="یک نویسنده کارمندی را انتخاب کنید")
    description = RichTextField(verbose_name="محتوای مقاله",help_text="محتوایی برای مقاله خود بنویسید")
    category = models.ManyToManyField(Category,verbose_name="دسته بندی",related_name="articles",help_text="کنترل یا فرمان را در مک نگه دارید تا بیش از یک مورد انتخاب شود|")
    thumbnail = models.ImageField(upload_to = 'images',verbose_name="تصویر مقاله",help_text='برای مقاله تصویری انتخاب کنید')
    publish = models.DateTimeField(default = timezone.now,verbose_name='زمان انتشار',help_text = 'فرمت صحیح تاریخ YYYY-MM-DD')
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 1,choices = STATUS_CHOICES,verbose_name='وضعیت',help_text="وضعیت مقاله را انتخاب کنید")
    hits = models.ManyToManyField(IPAddress,blank=True,related_name='hits',verbose_name='آدرس آی پی')
   
    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']
   
    def __str__(self):
        return self.title
    
    def jpublish(self):
        return jalali_conveter(self.publish)
    jpublish.short_description = "زمان انتشار"

    
    def thumbnail_tag(self):
        return format_html("<img src='{}' width=70px hieght=70px style='border-radius:10px'; >".format(self.thumbnail.url))
    thumbnail_tag.short_description = "تصویر مقاله"
    
    def category_to_str(self):
        return ", ".join([category.title for category in self.category.active()])
    category_to_str.short_description = "دسته بندی"
    
    def get_absolute_url(self):
        return reverse('account:home')
    
    
    objects= ArticleManager()
    
#   end model comment
#   start model comment

class Comment(models.Model):
    comment = models.CharField(max_length=10000,verbose_name="کامنت",help_text="نظر خود را بنویسید")
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,verbose_name="کاربر",help_text="کاربر خود را انتخاب کنید")
    active = models.BooleanField(default=False,verbose_name="فعال",help_text="در سایت نمایش داده شود ؟")
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="مقاله",help_text="لطفا یک مقاله برای نظر دادن انتخاب کنید")
    date = models.DateTimeField(default = timezone.now,verbose_name="تاریخ انتشار",help_text = 'فرمت صحیح تاریخ YYYY-MM-DD')
 
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظر ها'
        ordering = ['-date']
   
    
    def __str__(self):
        return self.comment[:30]
    
    def jpublish(self):
        return jalali_conveter(self.date)
    jpublish.short_description = "تاریخ انتشار"

#   end model comment

