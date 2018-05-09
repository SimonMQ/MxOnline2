from django.db import models
from datetime import datetime
from course.models import Course
from users.models import UserProfile


# Create your models here.
class UserAsk(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=20)
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    course_name = models.CharField(verbose_name="课程名", max_length=50)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户：{0} 的手机号:{1}'.format(self.name, self.mobile)


class CourseComment(models.Model):
    course = models.ForeignKey(Course, verbose_name="评论课程", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name="评论用户", on_delete=models.CASCADE)
    comment = models.CharField(verbose_name="评论内容", max_length=255)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})对于《{1}》的评论'.format(self.user, self.course)


class UserFavorite(models.Model):
    TYPE_CHOICES = (
        (1, '机构'),
        (2, '课程'),
        (3, '教师'),
    )
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    fav_id = models.IntegerField(verbose_name="收藏用户ID", default=0)
    fav_type = models.IntegerField(verbose_name="收藏类型", choices=TYPE_CHOICES, default=1)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})收藏了{1}'.format(self.user, self.fav_type)


class UserMessage(models.Model):
    # 为0则发送给所有用户，否则就是用户的id
    user = models.IntegerField(verbose_name="用户", default=0)
    message = models.CharField(verbose_name="消息内容", max_length=255)
    has_read = models.BooleanField(verbose_name="是否已读", default=False)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})接收了消息：{1}'.format(self.user, self.message)


class UserCourse(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0})学习了《{1}》'.format(self.user, self.course)
