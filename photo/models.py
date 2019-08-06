
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# User 모델은 확장 가능
# settings.AUTH_USER_MODEL

# from django.contrib.auth import get_user_model
# author = models.ForeignKey(get_user_model)

from django.urls import reverse
# url pattern 이름을 가지고 주소를 만들어주는 함수

# Create your models here.
# models.Model : ORM 관련 기능을 다 가지고 있다.
class Photo(models.Model):
    # ForeignKey(연결되는 모델, 삭제 시 동작, 연관 이름)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    # CASCADE : 연속해서 지운다. -> 탈퇴하면 사진도 지움
    # PROTECT : 사진이 남아있으면 탈퇴 불가 -> 탈퇴 프로세스에 사진을 삭제하고 탈퇴시킴
    # 특정값으로 셋팅

    # 글 삭제 : DB 로우, 레코드를 삭제 -> 메모리에 남아 있는 사진 삭제

    # related_name 으로 연관 데이터를 얻을 수 없다면 쿼리를 별도로 진행해야 한다. -> 내 프로필 페이지

    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')
    # upload_to : 함수를 사용해서 폴더를 동적으로 설정할 수 있다.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # like 정보 저장
    like = models.ManyToManyField(User, related_name='like_post', blank=True)

    # save 정보 저장
    favorite = models.ManyToManyField(User, related_name='save_post', blank=True)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        # detail/<int:pk>/
        return reverse('photo:detail', args=[self.id])


    # # save 를 실행하고 나면 DB 에 레코드 생성
    # # save 하기 전에 수행할 동작
    # # save 하고 나서 수행할 동작
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     # before
    #     super(Photo,self).save()
    #     # after
    #
    # # delete 를 실행하고 나면 DB 에서 레코드 제거
    # # delete 하기 전에 수행할 동작
    # # delete 하고 나서 수행할 동작
    # def delete(self, using=None, keep_parents=False):
    #     # before
    #     super(Photo,self).delete()
    #     # after

class Comment(models.Model):
    # TODO : 댓글 남기기를 위해서 form이 필요
    # TODO : Document의 뷰에서 처리
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    text = models.CharField(max_length=400)
    created = models.DateTimeField(auo_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.author.username if self.author else "무명") + "의 댓글"

    def get_absolute_url(self):
        return reverse('photo:detail', args=[self.id])