from django.contrib import admin
from .models import EmailVerifyRecord, Banner


# 可以复写AdminSite模型,调整site一些属性的值
# class MyAdminSite(admin.AdminSite):
#     site_title = 'Simon后台管理器'
#     site_header = 'Simon'
#
# admin_site = MyAdminSite(name='admin')

# 也可以直接在修改admin.site.site_title
# admin.site.index_title = 'Site administration'
admin.site.site_title = 'Simon后台管理器'
admin.site.site_header = 'Simon的公司'


# Register your models here.
class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ('code', 'email', 'send_type', 'send_time')
    search_fields = ('code', 'email', 'send_type')
    list_filter = ('code', 'email', 'send_type', 'send_time')


class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'url', 'index', 'add_time')
    search_fields = ('title', 'image', 'url', 'index')
    list_filter = ('title', 'image', 'url', 'index', 'add_time')


admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
admin.site.register(Banner, BannerAdmin)



