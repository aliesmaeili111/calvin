from django.urls import path
from .views import (ArticleList,
                    detail,CategoryList,
                    AuthorList,ArticlePreview,
                    ajax_save_comment,ajax_delete_comment,
                    SearchList,about,contactView)

app_name = 'blog'

urlpatterns = [
    path('', ArticleList.as_view(),name="home"),
    path('page/<int:page>', ArticleList.as_view(),name="home"),
    
    path('ajax-save-comment/', ajax_save_comment,name="save-comment"),
    path('ajax-delete-comment/', ajax_delete_comment,name="delete-comment"),
    
    path('article/<slug:slug>', detail,name="detail"),
    path('preview/<int:pk>', ArticlePreview.as_view(),name="preview"),
    
    path('category/<slug:slug>', CategoryList.as_view(),name="category"),
    path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(),name="category"),
   
    path('author/<slug:username>', AuthorList.as_view(),name="author"),
    path('author/<slug:username>/page/<int:page>', AuthorList.as_view(),name="author"),
   
    path('search/', SearchList.as_view(),name="search"),
    path('search/page/<int:page>', SearchList.as_view(),name="search"),
    
    path('about/', about,name="about"),
    
    path('contact/', contactView,name='contact'),
]
