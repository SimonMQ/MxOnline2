# coding:utf-8
from django.urls import path, re_path
from users.views import UserInfoView, UploadImageView, UpdatePwdView, \
    MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView


app_name = 'users'

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('upload/image/', UploadImageView.as_view(), name='upload_image'),
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),

    path('mycourse/', MyCourseView.as_view(), name='mycourse'),
    path('myfav/org/', MyFavOrgView.as_view(), name='myfav_org'),
    path('myfav/teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),
    path('myfav/course/', MyFavCourseView.as_view(), name='myfav_course'),
    path('mymessage/', MyMessageView.as_view(), name='mymessage'),
]

