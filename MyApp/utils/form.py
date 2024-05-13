from MyApp import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from MyApp.utils.bootstrap import BootStrapModelForm,BootStrapForm
from MyApp.utils.encrypt import md5

class RegisterForm(BootStrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True)
    )
    confirm_pwd = forms.CharField(
        label = '确认密码',
        widget = forms.PasswordInput(render_value=True)
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )
    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return username
    
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_pwd(self):
        pwd = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm_pwd')
        if md5(confirm) != pwd:
            raise ValidationError('密码不一致')
        return confirm
    
class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True   # 必填
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

class Movie_BoxModelForm(BootStrapModelForm):
    class Meta:
        model = models.movie_box
        fields = '__all__'
        exclude = ['box']


class CommentForm(BootStrapForm):
    content = forms.CharField(
        label='评论内容',
        widget=forms.TextInput(attrs={'style': 'width: 200%; height: 100px;','id':'comment_content'}),
        required=True,
    )
    movie_id = forms.CharField(
        label='电影id',
        required=False,
    )
    def clean_content(self):
        cleaned_content = self.cleaned_data.get('content')
        return cleaned_content
class RatingForm(BootStrapForm):
    rating = forms.CharField(
        label='评分',
        widget=forms.TextInput(attrs={'style': 'width: 200%; height: 100px;','id':'rating_content'}),
        required=True,
    )
    movie_id = forms.CharField(
        label='电影id',
        required=False,
    )