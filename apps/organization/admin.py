from django.contrib import admin
from .models import Organization, Teacher, City


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'add_time')
    search_fields = ('name', 'desc')
    list_filter = ('name', 'desc', 'add_time')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'click_nums', 'fav_nums', 'add_time')
    search_fields = ('name', 'desc', 'click_nums', 'fav_nums')
    list_filter = ('name', 'desc', 'click_nums', 'fav_nums', 'city__name', 'address', 'add_time')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'work_year', 'work_company', 'add_time')
    search_fields = ('name', 'organization', 'work_year', 'work_company')
    list_filter = ('name', 'organization__name', 'work_year', 'work_company', 'click_nums', 'fav_nums', 'add_time')


admin.site.register(City, CityAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Teacher, TeacherAdmin)