from django.contrib import admin
from .models import CourseOrg, Teacher, City


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'add_time')
    search_fields = ('name', 'desc')
    list_filter = ('name', 'desc', 'add_time')


class CourseOrgAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'click_nums', 'fav_nums', 'add_time')
    search_fields = ('name', 'desc', 'click_nums', 'fav_nums')
    list_filter = ('name', 'desc', 'click_nums', 'fav_nums', 'city__name', 'address', 'add_time')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'work_year', 'work_company', 'add_time')
    search_fields = ('name', 'organization', 'work_year', 'work_company')
    list_filter = ('name', 'org__name', 'work_year', 'work_company', 'click_nums', 'fav_nums', 'add_time')


admin.site.register(City, CityAdmin)
admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(Teacher, TeacherAdmin)