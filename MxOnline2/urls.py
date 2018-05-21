"""MxOnline2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
import users.urls, organization.urls, course.urls
from users.views import IndexView, LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView
from django.views.static import serve
from MxOnline2.settings import MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='active_user'),
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path('reset/(?P<reset_code>.*?)/', ResetPwdView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    path('captcha/', include('captcha.urls')),

    # 配置图片路径、静态文件路径
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    path('users/', include(users.urls, namespace='users')),
    path('organization/', include(organization.urls, namespace='organization')),
    path('course/', include(course.urls, namespace='course')),
    # 富文本ckeditor配置url
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

handler404 = 'users.views.pag_not_found'
handler500 = 'users.views.page_error'
