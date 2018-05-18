from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import City, Organization, Teacher
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from operation.models import UserAsk, UserFavorite


# Create your views here.
class OrgListView(View):
    def get(self, request):
        all_cities = City.objects.all()
        all_organizations = Organization.objects.all()

        hot_organizations = all_organizations.order_by('-click_nums')[:5]

        # 分类筛选
        category_id = request.GET.get('ct', '')
        if category_id:
            all_organizations = all_organizations.filter(category=category_id)

        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_organizations = all_organizations.filter(city=int(city_id))

        # 排序筛选
        sort_id = request.GET.get('sort', '')
        if sort_id == 'students':
            all_organizations = all_organizations.order_by('-learn_nums')
        elif sort_id == 'courses':
            all_organizations = all_organizations.order_by('-course_nums')

        course_org_nums = all_organizations.count()

        # 翻页功能
        paginator = Paginator(all_organizations, 3)
        page = request.GET.get('page')
        # try:
        #         #     # 获取页码内的列表信息
        #         #     organizations = paginator.page(page)
        #         # except PageNotAnInteger:
        #         #     # 如果用户请求的页码不是整数，显示第一页
        #         #     organizations = paginator.page(1)
        #         # except EmptyPage:
        #         #     # 如果用户请求的页码超过最大页码，显示最后一页
        #         #     organizations = paginator.page(paginator.num_pages)
        organizations = paginator.get_page(page)

        context = {
            'all_cities': all_cities,
            'all_organizations': organizations,
            'hot_organizations': hot_organizations,
            'course_org_nums': course_org_nums,
            'category_id': category_id,
            'city_id': city_id,
            'sort_id': sort_id,
        }
        return render(request, 'organization/org_list.html', context=context)


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 将form内容保存至UserAskModel，这里使用commit=True参数会将数据保存，为False则不保存至db。
            # user_ask是一个instance：userask_form类ModelForm所映射的数据库模型，即UserAskForm
            # 如果该对象已创建，则更新；如果该对象未创建，则新建。
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class AddFavView(View):
    def post(self, request):
        # 如果用户未登录，则提示用户未登录，ajax
        if not request.user.is_authenticated:
            return HttpResponse({'status': 'fail', 'msg': '用户未登录'}, content_type='application/json')

        # 获取收藏id即类型，如果数据库中已存在，那么取消收藏；
        id = request.POST.get('fav_id', None)
        type = request.POST.get('fav_type', None)
        if id and type:
            exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
            if exist_record:
                exist_record.delete()
                return HttpResponse({'status': 'success', 'msg': '收藏'}, content_type='application/json')
            else:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.save()
                return HttpResponse({'status': 'success', 'msg': '已收藏'}, content_type='application/json')
        else:
            return HttpResponse({'status': 'fail', 'msg': '收藏出错'}, content_type='application/json')


class OrgDetailHomeView(View):
    def get(self, request, org_id):
        organization = Organization.objects.get(id=int(org_id))
        organization.click_nums += 1
        organization.save()
        # ForeignKey的反向查询用_set方法
        all_courses = organization.course_set.all()[:4]
        all_teachers = organization.teacher_set.all()[:4]
        current = 'home'

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=organization.id, fav_type=1):
                has_fav = True

        context = {
            'organization': organization,
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'current': current,
            'has_fav': has_fav,
        }
        return render(request, 'organization/org_detail_home.html', context=context)


class OrgDetailCourseView(View):
    def get(self, request, org_id):
        organization = Organization.objects.get(id=int(org_id))
        # ForeignKey的反向查询用_set方法
        all_courses = organization.course_set.all()

        # 翻页功能
        paginator = Paginator(all_courses, 3)
        page = request.GET.get('page')
        all_courses = paginator.get_page(page)

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=organization.id, fav_type=1):
                has_fav = True

        current = 'course'
        context = {
            'organization': organization,
            'all_courses': all_courses,
            'current': current,
            'has_fav': has_fav,
        }
        return render(request, 'organization/org_detail_course.html', context=context)


class OrgDetailTeacherView(View):
    def get(self, request, org_id):
        organization = Organization.objects.get(id=int(org_id))
        # ForeignKey的反向查询用_set方法
        all_teachers = organization.teacher_set.all()

        # 翻页功能
        paginator = Paginator(all_teachers, 3)
        page = request.GET.get('page')
        all_teachers = paginator.get_page(page)

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=organization.id, fav_type=1):
                has_fav = True

        current = 'teacher'
        context = {
            'organization': organization,
            'all_teachers': all_teachers,
            'current': current,
            'has_fav': has_fav,
        }
        return render(request, 'organization/org_detail_teacher.html', context=context)


class OrgDetailDescView(View):
    def get(self, request, org_id):
        organization = Organization.objects.get(id=int(org_id))
        # ForeignKey的反向查询用_set方法
        current = 'desc'

        # 收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=organization.id, fav_type=1):
                has_fav = True

        context = {
            'organization': organization,
            'current': current,
            'has_fav': has_fav,
        }
        return render(request, 'organization/org_detail_desc.html', context=context)
