from django.db import models
from datetime import datetime
from organization.models import CourseOrg, Teacher
from django.utils.html import format_html


# Create your models here.
class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级'),
    )
    course_org = models.ForeignKey(CourseOrg, verbose_name="所属机构", on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, verbose_name="授课教师", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="名称", max_length=20)
    desc = models.CharField(verbose_name="课程描述", max_length=255)
    detail = models.TextField(verbose_name="课程详情")
    image = models.ImageField(verbose_name="封面图", upload_to='course/%Y/%m')
    degree = models.CharField(verbose_name="难度", choices=DEGREE_CHOICES, max_length=2, default='cj')
    is_banner = models.BooleanField(verbose_name="是否轮播", default=False)
    learn_times = models.IntegerField(verbose_name="课程时长(分钟数)", default=0)
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    learn_nums = models.IntegerField(verbose_name="学习人数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    category = models.CharField(verbose_name="分类", max_length=20)
    tag = models.CharField(verbose_name="标签", max_length=20)
    you_need_know = models.CharField(verbose_name="课程须知", max_length=255, default="本课程需要静心阅读")
    teacher_tell = models.CharField(verbose_name="老师告诉你", max_length=255, default="好好学习，天天向上")
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    # 设置某个字段的颜色
    def colored_degree(self):
        if self.degree == 'cj':
            color_code = 'green'
        elif self.degree == 'zj':
            color_code = 'yellow'
        elif self.degree == 'gj':
            color_code = 'red'
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            self.degree,
        )

    # short_description functions like a model field's verbose_name
    # 此方法用于自定义某个函数字段的标题
    colored_degree.short_description = u'难度'

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="所属课程", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="章节名", max_length=20)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="所属章节", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="视频名", max_length=20)
    # 这里的视频地址是否可以替换为一个FileField？
    url = models.URLField(verbose_name="视频地址", max_length=200, default='')
    learn_times = models.IntegerField(verbose_name="视频时长(分钟数)", default=0)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》章节的视频 >> {1}'.format(self.lesson, self.name)


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="所属课程", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="资源名", max_length=20)
    resource = models.FileField(verbose_name="资源文件", upload_to='course/resource/%Y%m')
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
