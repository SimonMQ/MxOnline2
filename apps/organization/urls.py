# coding:utf-8
from django.urls import path, re_path
from .views import OrgListView, AddUserAskView, OrgDetailHomeView, OrgDetailCourseView, OrgDetailTeacherView,\
    OrgDetailDescView, AddFavView, TeacherListView, TeacherDetailView


app_name = 'organization'

urlpatterns = [
    path('list/', OrgListView.as_view(), name='organization_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    path('add_fav', AddFavView.as_view(), name='add_fav'),
    re_path('home/(?P<org_id>\d+)/', OrgDetailHomeView.as_view(), name='org_detail_home'),
    re_path('course/(?P<org_id>\d+)/', OrgDetailCourseView.as_view(), name='org_detail_course'),
    re_path('org_teacher/(?P<org_id>\d+)/', OrgDetailTeacherView.as_view(), name='org_detail_teacher'),
    re_path('desc/(?P<org_id>\d+)/', OrgDetailDescView.as_view(), name='org_detail_desc'),
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name='teacher_detail'),
]


