import re
from django import forms
from operation.models import UserAsk


# 由于我们在UserAs模型中定义了该字段，所以此处不用再重新写一个Form，而是引用ModelForm。
# ModelForm的用法：先自定义一个继承自ModelForm的子类，然后在其中设置Meta元类，定义model属性为要关联的ORM模型
# 在fields中定义form表单中使用的字段,字段名必须是Model中的字段名.
# 另外，fields还有两个属性：fields = '__all__'和exclude = ['title']，分别代表引入所有字段和除掉某字段
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|176\d{8}$"
        pattern = re.compile(REGEX_MOBILE)
        if pattern.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')
