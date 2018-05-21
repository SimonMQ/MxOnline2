from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


# 注册页表单多了一个验证码字段captcha，从安装的第三方库django-simple-captcha引入
class RegisterForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})


class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']
