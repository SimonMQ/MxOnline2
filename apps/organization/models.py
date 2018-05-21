from django.db import models
from datetime import datetime


# Create your models here.
'''
points:
1、verbose_name的作用是给予对象一个人类可读的名字，”A human-readable name for the object“。
用于table中某个字段时，在admin后台会显示verbose_name，用于Meta中时，显示的是当前数据表的名称。
2、max_length为最大字符长度，由于CharField在数据库中对应为varchar，最大长度为255，
所以这里设置的最大值也不能超过255，否则，用TextField代替。max_length的计算方法:len("字符串")=3。
3、ImageField继承自FileField，用于上传文件，其中的upload_to属性，用于指定上传文件的目录，该目录会在MEDIA_ROOT下自动生成。
如使用upload_to='uploads/%Y/%m/%d/'，文件会上传到MEDIA_ROOT/uploads/2015/01/30中，
/%Y/%m/%d/为strftime()格式化的xxxx年xx月xx日。
4、null=True和blank=True通常一起使用，null代表数据库可以为空，blank代表后台表单数据填写时可以留白。
5、choices用于选择框，在使用前应该在class中定义一个可迭代对象，[(A, B), (A, B) ...]，每个元组中第一个
元素代表实际值，第二个是人类可读名称，类似于verbose_name。
'''


class City(models.Model):
    name = models.CharField(verbose_name="城市", max_length=20)
    desc = models.CharField(verbose_name="描述", max_length=255)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Organization(models.Model):
    ORG_CHOICES = (
        ('pxjg', '培训机构'),
        ('gx', '高校'),
        ('gr', '个人'),
    )

    name = models.CharField(verbose_name="机构名称", max_length=20)
    desc = models.TextField(verbose_name="机构描述")
    category = models.CharField(verbose_name="机构类别", max_length=20, choices=ORG_CHOICES, default='pxjg')
    tag = models.CharField(verbose_name="机构标签", max_length=20, default="全国知名")
    image = models.ImageField(verbose_name="封面图", upload_to='organization/%Y/%m')
    address = models.CharField(verbose_name="机构地址", max_length=200)
    city = models.ForeignKey(City, verbose_name="所在城市", on_delete=models.CASCADE)
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    learn_nums = models.IntegerField(verbose_name="学习人数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    course_nums = models.IntegerField(verbose_name="课程数", default=0)
    is_authentication = models.BooleanField(verbose_name="是否认证", default=False)
    is_gold = models.BooleanField(verbose_name="金牌机构", default=False)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 定义一个方法，可以获取当前机构的课程数目和教师数目
    # 也可以在view中写，但是重复造轮子，每次调用都要写，写在模型里方便调用
    def get_course_nums(self):
        return self.course_set.all().count()

    def get_teacher_nums(self):
        return self.teacher_set.all().count()


class Teacher(models.Model):
    organization = models.ForeignKey(Organization, verbose_name="所属机构", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="姓名", max_length=20)
    age = models.IntegerField(verbose_name="年龄", default=0)
    image = models.ImageField(verbose_name="头像", upload_to='teacher/%Y/%m', default='', null=True, blank=True)
    work_year = models.IntegerField(verbose_name="工作年限", default=0)
    work_company = models.CharField(verbose_name="就职公司", max_length=50)
    work_position = models.CharField(verbose_name="工作岗位", max_length=50)
    points = models.CharField(verbose_name="教学特点", max_length=50)
    click_nums = models.IntegerField(verbose_name="点击数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()
