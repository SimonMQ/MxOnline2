from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from users.models import UserProfile, EmailVerifyRecord, Banner
from course.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import Organization, Teacher
from django.db.models import Q
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UserInfoForm
from utils import send_email
from .forms import UploadImageForm
from django.http import HttpResponse
import json
from utils.mixin_utils import LoginRequiredMixin
from django.core.paginator import Paginator


# 首页视图
class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        organizations = Organization.objects.all()[:15]
        context = {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'organizations': organizations,
        }
        return render(request, 'index.html', context=context)


# 复写ModelBackend的authenticate方法。
# django自带的authenticate方法只能认证用户名，现在希望用户名和邮箱都可以登录.
"""
Authenticates against settings.AUTH_USER_MODEL.

def authenticate(self, request, username=None, password=None, **kwargs):
    if username is None:
        username = kwargs.get(UserModel.USERNAME_FIELD)
    try:
        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:
        # Run the default password hasher once to reduce the timing
        # difference between an existing and a nonexistent user (#20760).
        UserModel().set_password(password)
    else:
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
"""


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 登录页视图
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 先实例化一个Form对象，从request.POST所构建的字典中bound绑定数据
        # 然后调用Form.is_valid()方法，判断从前端传过来的数据是否合法
        # 如果数据合法，获取用户名和密码，然后进行后台验证。如果验证成功并且用户已激活则登录并转到主页，否则返回错误信息。
        # 如果数据不合法，则返回login页，并将用户填写的数据也放进去，且包含表单错误信息
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            user = authenticate(username=user_name, password=pass_word)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'login_form': login_form, 'msg': '用户名或密码错误'})
            else:
                return render(request, 'login.html', {'login_form': login_form, 'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


# 登出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


# 注册页视图
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        """业务逻辑：
        首先实例化一个Form对象，从request.POST中绑定数据，判断其是否合法
        如果合法，获取email和password，然后判断email是否已经存在，如果存在，则返回注册页并渲染一个信息。
        如果email可用，实例化一个UserProfile对象，并将数据保存至数据库，然后发送注册邮件，并然后登录页。
        如果form不合法，返回register页
        """
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', None)
            pass_word = request.POST.get('password', None)
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': 'register_form', 'msg': '邮箱已存在'})
            else:
                user_profile = UserProfile()
                user_profile.email = user_name
                user_profile.username = user_name
                user_profile.password = make_password(pass_word)
                user_profile.is_active = False
                user_profile.save()
                # 发送邮箱验证码
                send_email.send_user_email(email=user_name, send_type='register')
                return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 激活用户页视图
class ActiveUserView(View):
    """业务逻辑：
    获取从用户端传过来的code，判断数据库中是否存在，如果存在，激活该用户,并跳转到登陆页。否则跳转到激活失败页面
    """
    def get(self, request, active_code):
        email_record = EmailVerifyRecord.objects.filter(code=active_code)
        if email_record:
            # 这里有极小可能但是不排除出现两个验证码相同的情况，如果存在，说明之前的用户A已经激活，当前的用户B未激活，
            # 现在,直接将所有符合验证码的用户都激活就行了
            for record in email_record:
                email = record.email
                user_profile = UserProfile.objects.get(email=email)
                user_profile.is_active = True
                user_profile.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


# 忘记密码页视图
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forget_pwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            if UserProfile.objects.filter(email=email):
                send_email.send_user_email(email=email, send_type='forget')
                # 成功之后要用重定向,否则直接render的话,地址栏还是显示的/forget/
                return render(request, "login.html", {"msg": "重置密码邮件已发送,请注意查收"})
            else:
                return render(request, 'forget_pwd.html', {'forget_form': forget_form, 'msg': '邮箱错误'})
        else:
            return render(request, 'forget_pwd.html', {'forget_form': forget_form})


# 重置密码页视图
class ResetPwdView(View):
    def get(self, request, reset_code):
        reset_record = EmailVerifyRecord.objects.filter(code=reset_code)
        if reset_record:
            for record in reset_record:
                email = record.email
                return render(request, 'reset_pwd.html', {'email': email})
        else:
            return render(request, 'active_fail.html')


# 修改密码页视图
# 紧跟ResetPwdView，由于重置密码的链接中含有一个reset_code，所以，提交表单时的post方式并不适应
# 这里新建一个View，专门用来处理reset_pwd.html页面提交过来的form信息
class ModifyPwdView(View):
    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        email = request.POST.get('email', None)
        if reset_form.is_valid():
            password1 = request.POST.get('password1', None)
            password2 = request.POST.get('password2', None)
            if password1 == password2:
                user_profile = UserProfile.objects.get(email=email)
                user_profile.password = make_password(password1)
                user_profile.save()
                return HttpResponseRedirect(reverse('login'))
            else:
                return render(request, 'reset_pwd.html', {'email': email, 'reset_form': reset_form, 'msg': '两次输入的密码不一致'})
        else:
            return render(request, 'reset_pwd.html', {'email': email, 'reset_form': reset_form})


# 用户中心页
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/usercenter_info.html')

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(View):
    def post(self, request):
        upload_image_form = UploadImageForm(request.POST, request.FILES)
        if upload_image_form.is_valid():
            image = upload_image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UpdatePwdView(View):
    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            password1 = request.POST.get('password1', None)
            password2 = request.POST.get('password2', None)
            if password1 == password2:
                user_profile = request.user
                user_profile.password = make_password(password1)
                user_profile.save()
                return HttpResponse('{"status": "success"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "密码不一致"}',  content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')


class MyCourseView(View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        context = {
            'user_courses': user_courses,
        }
        return render(request, 'users/usercenter_mycourse.html', context=context)


class MyFavOrgView(View):
    def get(self, request):
        user_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=1)
        org_ids = [user_fav_org.fav_id for user_fav_org in user_fav_orgs]
        my_fav_orgs = Organization.objects.filter(id__in=org_ids)
        context = {
            'my_fav_orgs': my_fav_orgs,
        }
        return render(request, 'users/usercenter_fav_org.html', context=context)


class MyFavTeacherView(View):
    def get(self, request):
        user_fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        teacher_ids = [user_fav_teacher.fav_id for user_fav_teacher in user_fav_teachers]
        my_fav_teachers = Teacher.objects.filter(id__in=teacher_ids)
        context = {
            'my_fav_teachers': my_fav_teachers,
        }
        return render(request, 'users/usercenter_fav_teacher.html', context=context)


class MyFavCourseView(View):
    def get(self, request):
        user_fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=2)
        course_ids = [user_fav_course.fav_id for user_fav_course in user_fav_courses]
        my_fav_courses = Course.objects.filter(id__in=course_ids)
        context = {
            'my_fav_courses': my_fav_courses,
        }
        return render(request, 'users/usercenter_fav_course.html', context=context)


class MyMessageView(View):
    def get(self, request):
        user_messages = UserMessage.objects.filter(user=request.user.id)

        # 翻页功能
        paginator = Paginator(user_messages, 3)
        page = request.GET.get('page')
        user_messages = paginator.get_page(page)

        context = {
            'my_messages': user_messages,
        }
        return render(request, 'users/usercenter_message.html', context=context)


def pag_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
