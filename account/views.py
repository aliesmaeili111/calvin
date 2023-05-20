from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from blog.models import Article
from .mixins import (FieldsMixin,
                     FormValidMixin,
                    AuthorAccessMixin,
                    SuperUserAccessMixin,
                    AuthorsAccessMixin)
from django.urls import reverse_lazy
from account.models import User
from account.forms import (ProfileForm,SignupForm,CommentForm)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import (urlsafe_base64_encode,
                               urlsafe_base64_decode)
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from blog.models import Comment
from django.db.models import Q


class ArticleList(AuthorsAccessMixin,ListView):
    
    paginate_by = 20
    template_name = 'registration/home.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)
        
class ArticleCreate(SuccessMessageMixin,AuthorsAccessMixin,FormValidMixin,FieldsMixin,CreateView):

    model = Article
    template_name = 'registration/article-create-update.html'
    success_url = reverse_lazy('account:home')
    success_message = "مقاله ایجاد شد" 
    
    
class ArticleUpdate(SuccessMessageMixin,AuthorAccessMixin,FormValidMixin,FieldsMixin,UpdateView):
        
    model = Article
    template_name = 'registration/article-create-update.html'
    success_message = "مقاله تغییر یافت"
    
    
class ArticleDelete(SuperUserAccessMixin,SuccessMessageMixin,DeleteView):
    
    model = Article
    template_name = 'registration/article_confirm_delete.html'
    success_message = "با موفقیت مقاله حذف شد"
    success_url = reverse_lazy('account:home')
    
class Profile(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')
    success_message = 'اطلاعات شما با موفقیت تغییر یافت'
    
    
    def get_object(self):
        
        return User.objects.get(pk = self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(Profile,self).get_form_kwargs()
        kwargs.update({
            'user':self.request.user
            })
        return kwargs 
    

    
class Login(SuccessMessageMixin,LoginView):
    success_message = "با موفقیت وارد شدید"

    def get_success_url(self):
        user = self.request.user
        
        if user.is_superuser or user.is_author :
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')



class Register(CreateView):
    form_class = SignupForm
    template_name = "registration/register.html"
    
    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
    
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('registration/account_activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
        })
        
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
        email.send()
        return render(self.request,'registration/active_email.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request,'registration/active_link.html')
    else:
        return render(request,'registration/deactive_link.html')


class CommentList(AuthorsAccessMixin,ListView):
    paginate_by = 20
    template_name = 'registration/home_comment.html'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Comment.objects.all()
        else:
            return Comment.objects.filter(user=self.request.user)


class CommentCreate(SuccessMessageMixin,LoginRequiredMixin,CreateView):

    model = Comment
    template_name = 'registration/comment.html'
    form_class = CommentForm
    success_url = reverse_lazy('account:comment_list')
    success_message = "نظر شما ثبت شد " 
    
    def get_object(self):
        return Comment.objects.get(pk = self.request.user.pk)
    
    
class SearchListArticle(ListView):

    template_name = "registration/search_list_home.html"
    paginate_by =  20
    
    def get_queryset(self):
        global search
        search = self.request.GET.get('q')
        return Article.objects.filter(Q(description__icontains = search) | Q(title__icontains = search))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = search
        return context
