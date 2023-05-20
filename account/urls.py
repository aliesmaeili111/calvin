from django.urls import path
from django.contrib.auth import views
from account.views import (ArticleList,
                           ArticleCreate,
                           ArticleUpdate,
                           ArticleDelete,
                           Profile,
                           CommentCreate,
                           CommentList,
                           SearchListArticle)

app_name = 'account'

urlpatterns = [
    path('',ArticleList.as_view(), name='home'),
    path('article/create',ArticleCreate.as_view(), name='article-create'),
    path('article/update/<int:pk>/',ArticleUpdate.as_view(), name='article-update'),
    path('article/delete/<int:pk>/',ArticleDelete.as_view(), name='article-delete'),
    path('profile/',Profile.as_view(), name='profile'),
    path('comment/create/',CommentCreate.as_view(), name='comment'),
    path('comment/',CommentList.as_view(), name='comment_list'),
    path('search/',SearchListArticle.as_view(), name='search'),
]
