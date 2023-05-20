from django import template
from ..models import Category,Article
from django.db.models import Count


register = template.Library()



@register.inclusion_tag('blog/partials/category_navbar.html')
def cetagory_navbar():
    return  {
        'category': Category.objects.filter(status=True),
    }
    
    
    
@register.inclusion_tag('registration/partials/link.html')
def link(request,link_name,content,icon):
    return {
        "request":request,
        "link_name":link_name,
        'link': 'account:{}'.format(link_name),
        "content":content,
        "icon":icon,

    }
    
@register.inclusion_tag('blog/partials/popular_articles.html')
def popular_articles():

    return  {
        'popular_articles': Article.objects.published().annotate(count=Count('id')).order_by('-count','-publish')[:2]
    }
    