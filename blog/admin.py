from django.contrib import admin
from blog.models import Article,Category,Comment,Contact,IPAddress
from account.models import User
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from jalali_date.admin import ModelAdminJalaliMixin 

# change admin site header
admin.site.site_header = "کالوین وبلاگ"


# start action in panel admin

def make_published(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status="p")
    if rows_updated == 1 :
        message_bit = ' منتشر شد.'
    else:
        message_bit = ' منتشر شدند'
    modeladmin.message_user(request,f"{rows_updated}مقاله {message_bit}")
    
make_published.short_description ="انتشار مقالات انتخاب شده"

    
def make_draft(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status="d")
    if rows_updated == 1 :
        message_bit = ' پیش نویس شد.'
    else:
        message_bit = ' پیش نویس شدند'
    modeladmin.message_user(request,f"{rows_updated}مقاله {message_bit}") 
    
make_draft.short_description ="پیش نویس شدن مقالات انتخاب شده"    

def make_active(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status=True)
    if rows_updated == 1 :
        message_bit = ' نمایش داده شد.'
    else:
        message_bit = ' نمایش داده شدند'
    modeladmin.message_user(request,f"{rows_updated}دسته بندی {message_bit}")
    
make_active.short_description ="نمایش دسته بندی انتخاب شده"

def make_not_active(modeladmin,request,queryset):
    
    rows_updated = queryset.update(status=False)
    if rows_updated == 1 :
        message_bit = ' نمایش داده نمیشه.'
    else:
        message_bit = ' نمایش داده نمیشوند'
    modeladmin.message_user(request,f"{rows_updated}دسته بندی {message_bit}")
    
make_not_active.short_description =" لغو نمایش دسته بندی انتخاب شده"

# end action in panel admin  
    
# star article admin

@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin,ModelAdminJalaliMixin,admin.ModelAdmin):
    
    def formfield_for_foreignkey(self,db_field,request,**kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super(ArticleAdmin,self).formfield_for_foreignkey(db_field,request,**kwargs)
    
    list_display = ('name_colored','thumbnail_tag','author_name','slug','jpublish','status','category_to_str')
    list_display_links = ('name_colored','slug','thumbnail_tag')
    list_filter = ('publish', 'category','status','author')
    list_editable = ('status',)
    search_fields =  ('title','descriptoin','slug','author')
    prepopulated_fields = {'slug':('title',)} 
    list_per_page = 15
    actions = [make_published,make_draft]
    date_hierarchy = 'publish'

    
 
    def author_name(self,obj):
        return obj.author.first_name +' '+ obj.author.last_name
    author_name.short_description = "نویسنده"
    
    def name_colored(self,obj):
        if obj.status == 'p':
            color_code = '447e9b'
        else:
            color_code = 'FF0000'
        html ="<span style='color:#{}'>{}</span>".format(color_code,obj.title[:30])
        return format_html(html)
    name_colored.short_description = "عنوان"
    
# end article admin
     
# star category admin

@admin.register(Category)  
class CategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    
    list_display = ('title','slug','status')
    list_display_links = ('title','slug')
    list_filter = (['status',])
    list_editable = ('status',)
    search_fields =  ('title','slug','position')
    prepopulated_fields = {'slug':('title',)}
    list_per_page = 10
    actions = [make_active,make_not_active]

# end category admin

# start action in panel admin for comment


def make_active_comment(modeladmin,request,queryset):
    
    rows_updated = queryset.update(active=True)
    if rows_updated == 1 :
        message_bit = ' فعال شد.'
    else:
        message_bit = ' فعال شدند'
    modeladmin.message_user(request,f"{rows_updated}نظر {message_bit}")
    
make_active_comment.short_description ="فعال کردن نظر های انتخاب شده"


def make_not_active_comment(modeladmin,request,queryset):
    
    rows_updated = queryset.update(active=False)
    if rows_updated == 1 :
        message_bit = ' غیر فعال شد.'
    else:
        message_bit = ' غیر فعال شدند'
    modeladmin.message_user(request,f"{rows_updated}نظر {message_bit}")
    
make_not_active_comment.short_description =" غیر فعال کردن نظر های انتخاب شده"

# end actions for comment

# star comment admin

@admin.register(Comment)  
class CommentAdmin(ImportExportModelAdmin,ModelAdminJalaliMixin,admin.ModelAdmin):
    
    def formfield_for_foreignkey(self,db_field,request,**kwargs):
        if db_field.name == 'article':
            kwargs['queryset'] = Article.objects.filter(status='p')
        return super(CommentAdmin,self).formfield_for_foreignkey(db_field,request,**kwargs)
    
    
    list_display = ['comment','user','jpublish','active','article']
    list_display_links = ('comment','user')
    list_editable = ('active',)
    list_filter = ('user',)
    search_fields =  ('comment','user')
    date_hierarchy = 'date'
    list_per_page = 10
    actions = [make_active_comment,make_not_active_comment]

# end comment admin


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','context')
    list_filter = ('name','email')
    search_fields = ('name','email')
    list_per_page = 20

admin.site.register(Contact,ContactAdmin)

class IPaddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address',)
    list_filter = ('ip_address',)
    search_fields = ('ip_address',)
    list_per_page = 20

admin.site.register(IPAddress,IPaddressAdmin)