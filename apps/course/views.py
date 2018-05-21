from django.shortcuts import render
from django.views.generic import View
from .models import Course, Video
from operation.models import UserFavorite, CourseComment, UserCourse
from django.core.paginator import Paginator
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all()

        hot_courses = all_courses.order_by('-click_nums')[:5]

        # sort
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('-learn_nums')

        # 搜索功能，使用icontain查询
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))

        # 翻页功能
        paginator = Paginator(all_courses, 3)
        page = request.GET.get('page')
        all_courses = paginator.get_page(page)

        context = {
            'all_courses': all_courses,
            'hot_courses': hot_courses,
            'sort': sort,
        }
        return render(request, 'course/course_list.html', context=context)


# Create your views here.
class CourseView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        organization = course.organization
        # 课程点击数+1
        course.click_nums += 1
        course.save()

        # 用户收藏功能，如果用户未登录，显示未收藏；用户已登录，可根据用户的收藏数据判断
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=2):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=organization.id, fav_type=1):
                has_fav_org = True

        # 相关课程推荐为根据标签推荐，需要排除自身
        tag = course.tag
        all_related_courses = Course.objects.filter(tag=tag)[:5]
        # 移除当前课程。待修改
        related_courses = all_related_courses

        context = {
            'course': course,
            'organization': organization,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        }
        return render(request, 'course/course_detail.html', context=context)


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        teacher = course.teacher

        # 关联数据，如果用户未学习该课程，则新建
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            UserCourse.objects.create(user=request.user, course=course)

        # 获取用户相关课程的方法：
        # 首先，获取所有course=当前课程的usercourse，在这些usercourse中获取所有用户的id
        # 其次，通过user_ids获取这些用户学过的所有usercourse，在其中获取所有的课程id
        # 然后，通过course_ids获取所有课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        # __in方法获取一个列表中的数据，filter查找所有匹配的对象
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        context = {
            'course': course,
            'teacher': teacher,
            'related_courses': related_courses,
        }
        return render(request, 'course/course_video.html', context=context)


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        teacher = course.teacher
        all_comments = course.coursecomment_set.all()

        # 关联数据，如果用户未学习该课程，则新建
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            UserCourse.objects.create(user=request.user, course=course)

        # 获取用户相关课程的方法：
        # 首先，获取所有course=当前课程的usercourse，在这些usercourse中获取所有用户的id
        # 其次，通过user_ids获取这些用户学过的所有usercourse，在其中获取所有的课程id
        # 然后，通过course_ids获取所有课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        # __in方法获取一个列表中的数据，filter查找所有匹配的对象
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        context = {
            'course': course,
            'teacher': teacher,
            'all_comments': all_comments,
            'related_courses': related_courses,
        }
        return render(request, 'course/course_comment.html', context=context)


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comment = request.POST.get("comments", "")
        if int(course_id) > 0 and comment:
            # 实例化一个course_comments对象
            course_comment = CourseComment()
            course = Course.objects.get(id=int(course_id))
            # 保存到数据库
            course_comment.course = course
            course_comment.user = request.user
            course_comment.comment = comment
            course_comment.save()
            return HttpResponse('{"status": "success", "msg": "评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "评论失败"}', content_type='application/json')


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        course.learn_nums += 1
        course.save()

        # 关联数据，如果用户未学习该课程，则新建
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            UserCourse.objects.create(user=request.user, course=course)

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user_id for user_course in user_courses]
        # __in方法获取一个列表中的数据，filter查找所有匹配的对象
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        context = {
            'video': video,
            'course': course,
            'related_courses': related_courses,
        }
        return render(request, 'course/course_play.html', context=context)
