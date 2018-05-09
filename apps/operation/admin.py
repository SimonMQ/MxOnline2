from django.contrib import admin
from .models import UserAsk, UserFavorite, CourseComment, UserMessage, UserCourse


class UserAskAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'course_name', 'add_time')
    search_fields = ('name', 'mobile', 'course_name')
    list_filter = ('name', 'mobile', 'course_name', 'add_time')


class UserCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'add_time')
    search_fields = ('user', 'course')
    list_filter = ('user', 'course', 'add_time')


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'has_read', 'add_time')
    search_fields = ('user', 'message', 'has_read')
    list_filter = ('user', 'message', 'has_read', 'add_time')


class CourseCommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'comment', 'add_time')
    search_fields = ('user', 'course', 'comment')
    list_filter = ('user', 'course', 'comment', 'add_time')


class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'fav_id', 'fav_type', 'add_time')
    search_fields = ('user', 'fav_id', 'fav_type')
    list_filter = ('user', 'fav_id', 'fav_type', 'add_time')


# 将后台管理器与models进行关联注册
admin.site.register(UserAsk, UserAskAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(CourseComment, CourseCommentsAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)
