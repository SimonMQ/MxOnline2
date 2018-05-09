from django.contrib import admin
from .models import Course, Lesson, Video, CourseResource


# Register your models here.
# 在admin后台注册模型，并且定制后台
class CourseAdmin(admin.ModelAdmin):
    # 设置fieldsets 控制管理“添加”和 “更改” 页面的布局，顺便可以给这些字段排序
    fieldsets = (
        (None, {
            'fields': ('name', 'desc', 'tag', 'is_banner', ('course_org', 'teacher'), 'degree', 'learn_times', ('click_nums', 'learn_nums', 'fav_nums'), 'category')
        }),
        ('其它选项', {
            'fields': ('detail', 'image', 'you_need_know', 'teacher_tell', 'add_time')
        }),
    )

    # 指定修改页面上显示的字段，如果不指定，则只显示__str__()指定的那一列。
    list_display = ('name', 'desc', 'course_org', 'teacher', 'is_banner', 'colored_degree', 'learn_times', 'learn_nums')
    search_fields = ('name', 'desc', 'detail', 'degree', 'learn_nums')
    list_filter = ('name', 'desc', 'detail', 'degree', 'learn_times', 'learn_nums')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'add_time')
    search_fields = ('course', 'name')
    # 由于course是一个外键，所以过滤的时候根据课程名称过滤，即course.name
    list_filter = ('course__name', 'name', 'add_time')


class VideoAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'name', 'add_time')
    search_fields = ('lesson', 'name')
    list_filter = ('lesson', 'name', 'add_time')


class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'resource', 'add_time')
    search_fields = ('course', 'name', 'resource')
    list_filter = ('course__name', 'name', 'resource', 'add_time')


# models与admin关联注册
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(CourseResource, CourseResourceAdmin)