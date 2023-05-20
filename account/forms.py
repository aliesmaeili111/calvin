from django import forms
from account.models import User
from blog.models import Article,Comment
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from captcha.fields import ReCaptchaField
from decouple import config


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','special_user','is_author','photo']
        
        
    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user')
        super(ProfileForm,self).__init__(*args,**kwargs)
        self.fields['special_user'] = JalaliDateField(label=("کاربر ویژه تا تاریخ"),widget=AdminJalaliDateWidget)
        
        
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['special_user'].disabled = True
            self.fields['is_author'].disabled = True
            
        
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200,help_text="لطفا ایمیل معتبر وارد کنید")
    
    captcha = ReCaptchaField(
    public_key= config('public_key'),
    private_key= config('private_key'),
    
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','captcha')
        
        
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment', 'user', 'active','article',"date")
        
    def __init__(self,*args,**kwargs):
        super(CommentForm,self).__init__(*args,**kwargs)
        self.fields['date'] = JalaliDateField(label=("تاریخ"),widget=AdminJalaliDateWidget)
