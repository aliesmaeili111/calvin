from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Article,Category,Comment,Contact
from django.core.paginator import Paginator
from django.views.generic import ListView,DetailView
from account.models import User
from django.contrib import messages
from account.mixins import AuthorAccessMixin 
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.mail import EmailMessage


class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 6

    
def detail(request,slug):
    article = get_object_or_404(Article.objects.published(),slug=slug)
    context = {
        'article': article,
        'comment': Comment.objects.filter(active=True,article=article).order_by('-date'),
    }
    
    ip_address = request.user.ip_address
    if ip_address not in article.hits.all():
        article.hits.add(ip_address)
        
    return render(request,'blog/article_detail.html',context)


def ajax_save_comment(request):
    if request.method == "POST":
        pk = request.POST.get('id')
        
        comment = request.POST.get('comment')
        article = Article.objects.get(id=pk)
        user = request.user
        
        new_comment = Comment.objects.create(comment=comment,user=user,article=article,active=True)
        new_comment.save()
        
        response = 'Comment Posted'
        return HttpResponse(response)
    
    

@csrf_exempt
def ajax_delete_comment(request):
    if request.method == "POST":
        id = request.POST.get('cid')
        comment = Comment.objects.get(id=id)
        comment.delete()
        
        return JsonResponse({"status":1})
    
    else:
        return JsonResponse({"status":2})


class CategoryList(ListView):
    template_name = "blog/category_list.html"
    paginate_by = 9
    
    def get_queryset(self):
        global category
        slug  = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(),slug=slug) 
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    template_name = "blog/author_list.html"
    paginate_by =  9
    
    def get_queryset(self):
        global author
        username  = self.kwargs.get('username')
        author = get_object_or_404(User,username=username)  
       
        return author.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
    
    
class ArticlePreview(AuthorAccessMixin,DetailView):
    template_name = "blog/article_detail.html"
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article,pk=pk)


class SearchList(ListView):
    template_name = "blog/search_list.html"
    paginate_by =  9
    
    def get_queryset(self):
        global search
        search = self.request.GET.get('q')
        return Article.objects.filter(Q(description__icontains = search) | Q(title__icontains = search))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = search
        return context

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def about(request):
    return render(request,'blog/about.html')

def contactView(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        context = request.POST['context']
            
        contact = Contact(name=name,email=email,context=context)

        contact.save()
        messages.success(request,'بزودی با شما تماس خواهیم گرفت')

    return render(request,'blog/contact.html')
        