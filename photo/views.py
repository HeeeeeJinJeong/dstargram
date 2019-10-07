from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
# 뷰를 실행하기 전에 특정한 로직을 추가로 실행하고 싶을 때 사용
# 로그인 여부, csrf 체크를 수행할것인지?
# 믹스인 : 클래스형 뷰
# 데코레이터 : 함수형 뷰

from .models import *

class PhotoList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'
    # paginate_by = 2


class PhotoMyList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = user.photos.all()
        return queryset


class PhotoLikeList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def get_queryset(self):
        # 로그인 한 유저가 좋아요를 클릭한 글을 찾아서 반환
        user = self.request.user
        queryset = user.like_post.all()
        return queryset


class PhotoSaveList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def get_queryset(self):
        # 로그인 한 유저가 저장을 클릭한 글을 찾아서 반환
        user = self.request.user
        queryset = user.save_post.all()
        return queryset

class PhotoCreate(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['text', 'image']
    template_name = 'photo/photo_create.html'
    success_url = '/'

    def form_valid(self, form):
        # 입력된 자료가 올바른지 채크
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            # 올바르다면
            # form : 모델 폼
            form.instance.save()
            return redirect('/')
        else:
            # 올바르지 않다면
            return self.render_to_response({'form':form})

class PhotoUpdate(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['text', 'image']
    template_name = 'photo/photo_update.html'

    def dispatch(self, request, *args, **kwargs):
        # 사용자가 접속했을 때 get인지, post인지 등을 결정하고 분기하는 부분

        object = self.get_object()

        if object.author != request.user:
            messages.warning(request, "수정할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)


from django.http import HttpResponseRedirect
from django.contrib import messages

class PhotoDelete(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photo/photo_delete.html'
    success_url = '/'

    # Life Cycle - ios, android, vue, react, django, fails
    # Framework 는 Life Cycle이 존재 : 어떤 순서로 구동이 되느냐?
    # URLConf -> View -> Model 순서
    # 어떤 뷰를 구동할 때 그 안에서 동작하는 순서
    def dispatch(self, request, *args, **kwargs):
        # 사용자가 접속했을 때 get인지, post인지 등을 결정하고 분기하는 부분

        object = self.get_object()

        if object.author != request.user:
            # 1) 삭제 페이지에서 권한이 없다 출력
            # 2) 디테일 페이지로 다시 돌아가서 삭제 실패 출력
            messages.warning(request, "삭제할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

    # # 로직을 수행하고, 템플릿을 랜더링 한다.
    # def get(self, request, *args, **kwargs):
    #     pass
    #
    # def post(self, request, *args, **kwargs):
    #     pass


    # def det_object(self, queryset=None):
    #     # 해당 쿼리셋을 이용해서 현재 페이지에 필요한 object를 인스턴스화 한다.
    #     pass
    #
    # def get_queryset(self):
    #     # 어떻게 데이터를 가져올 것이냐?
    #     pass

class PhotoDetail(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photo/photo_detail.html'

    def photo_detail(request, photo_id):
        photo = Photo.objects.get(pk=photo_id)
        comment_form = CommentForm()
        comments = photo.comments.all()
        return render(request,
                      {'object': photo, 'comments': comments, 'comment_form': comment_form})


from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse

class PhotoLike(View):
    def get(self, request, *args, **kwargs):

        # like를 할 정보가 있다면 진행, 없다면 중단
        if not request.user.is_authenticated:
            return HttpResponseForbidden
        else:
            # 1) 어떤 포스팅에?
            # 1-1) url : www.naver.com/blog/like/?photo_id=1
            # request.GET.get('photo_id')

            # 1-2) url : www.naver.com/blog/like/1
            # path('blog/like/<int:photo_id>/')
            # kwargs['photo_id']
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)

                # 2) 누가?
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)

            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path

            return HttpResponseRedirect(path)


class PhotoSave(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user

                if user in photo.favorite.all():
                    photo.favorite.remove(user)
                else:
                    photo.favorite.add(user)

            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path

            return HttpResponseRedirect(path)

# signal
# 1. 어떤 시그널이 발생했을 때 반응할 것인지?
# 2. 해당 시그널이 발생한 여부 확인

from django.db.models.signals import post_delete
from django.dispatch import receiver

import boto3
from django.conf import settings


@receiver(post_delete, sender=Photo) # 어떤 시그널이 발생헀는지, 누가 발생시켰는지
def post_delete(sender, instance, **kwargs):
    storage = instance.image.storage

    if storage.exists(str(instance.image)):
        storage.delete(str(instance.image))

    # session = boto3.Session(
    #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #     region_name=settings.AWS_REGION,
    # )
    #
    # s3 = session.resource('s3')
    #
    # # s3 Object : s3 에 업로드 된 파일 객체를 얻어도는 클래스
    # # arg1 : 버킷네임
    # # arg2 : 파일경로 - key
    # image = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, "media/"+str(instance.image)) # 버킷 네임, 파일경로
    # image.delete();;;

from .forms import CommentForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404

# ajax사용해서 댓글 달기
def comment_create(request, photo_id):
    # ajax 기능에 의해 호출된 것인지 구분하기 위한 값
    is_ajax = request.POST.get('is_ajax')

    photo = get_object_or_404(Photo, pk=photo_id)
    comment_form = CommentForm(request.POST)
    comment_form.instance.author_id = request.user.id
    comment_form.instance.photo_id = photo_id
    if comment_form.is_valid():
        comment = comment_form.save()

    # 만약 ajax 가 호출되었다면 redirection 없이 Json 형태로 응답
    if is_ajax:
        # 데이터 만들어서 던져주기
        html = render_to_string('photo/comment/comment_single.html', {'comment':comment})
        return JsonResponse({'html':html})
    return redirect(photo)

def comment_update(request, comment_id):
    is_ajax, data = (request.GET.get('is_ajax'), request.GET) if 'is_ajax' in request.GET else (request.POST.get('is_ajax', False), request.POST)

    comment = get_object_or_404(Comment, pk=comment_id)
    photo = get_object_or_404(Photo, pk=comment.photo.id)
    # user.is_staff
    # user.is_superuser
    if request.user != comment.author:
        messages.warning(request, "권한 없음")
        return redirect(photo)

    if is_ajax:
        form = CommentForm(data, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({"works": True})

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(photo)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'photo/comment/comment_update.html', {'form': form})


def comment_delete(request, comment_id):
    is_ajax = request.GET.get('is_ajax') if 'is_ajax' in request.GET else request.POST.get('is_ajax',False)
    comment = get_object_or_404(Comment, pk=comment_id)
    photo = get_object_or_404(Photo, pk=comment.photo.id)

    if request.user != comment.author and not request.user.is_staff and request.user != photo.author:
        messages.warning(request, "권한 없음")
        return redirect(photo)

    if is_ajax:
        comment.delete()
        return JsonResponse({"works":True})

    if request.method == "POST":
        comment.delete()
        return redirect(photo)
    else:
        return render(request, 'photo/comment/comment_delete.html', {'object': comment})
