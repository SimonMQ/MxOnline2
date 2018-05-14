from random import Random
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from MxOnline2.settings import EMAIL_FROM


# 随机生成一个n为的字符串
def random_str(random_length=8):
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    str = ''
    for n in range(random_length):
        random_int = Random().randint(0, (len(chars) - 1))
        random_char = chars[random_int]
        str += random_char
    return str


# 发送邮件
def send_user_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'Simon注册激活链接'
        email_body = '请点击下面的链接完成注册：http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = 'Simon重置密码链接'
        email_body = '请点击下面的链接完成重置密码：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
