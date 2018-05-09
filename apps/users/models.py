from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    nick_name = models.CharField(verbose_name="昵称", max_length=20)
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", choices=GENDER_CHOICES, max_length=6, default='male')
    address = models.CharField(verbose_name="地址", max_length=100, default='')
    mobile = models.CharField(verbose_name="手机号", max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name="头像", upload_to='image/%Y/%m', default='')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    VERIFY_RECORD_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码'),
        ('update_email', '修改邮箱'),
    )
    code = models.CharField(verbose_name="验证码", max_length=20)
    email = models.EmailField(verbose_name="邮箱", max_length=100)
    send_type = models.CharField(verbose_name="验证码类型", choices=VERIFY_RECORD_CHOICES, max_length=20)
    send_time = models.DateTimeField(verbose_name="", default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(verbose_name="标题", max_length=100)
    image = models.ImageField(verbose_name="轮播图", upload_to='banner/%Y/%m')
    url = models.URLField(verbose_name="访问地址", max_length=200)
    index = models.IntegerField(verbose_name="顺序", default=100)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}(位于第{1}位)'.format(self.title, self.index)
