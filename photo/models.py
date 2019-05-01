from django.db import models
from django.contrib.auth.models import User

# User 모델은 확장 가능
# settings.AUTH_USER_MODEL

# from django.contrib.auth import get_user_model
# author = models.ForeignKey(get_user_model)

from django.urls import reverse
# url pattern 이름을 가지고 주소를 만들어주는 함수

# Create your models here.
class Photo(models.Model):
    # ForeignKey(연결되는 모델, 삭제 시 동작, 연관 이름)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    # CASCADE : 연속해서 지운다. -> 탈퇴하면 사진도 지움
    # PROTECT : 사진이 남아있으면 탈퇴 불가 -> 탈퇴 프로세스에 사진을 삭제하고 탈퇴시킴
    # 특정값으로 셋팅

    # related_name 으로 연관 데이터를 얻을 수 없다면 쿼리를 별도로 진행해야 한다. -> 내 프로필 페이지

    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')
    # upload_to : 함수를 사용해서 폴더를 동적으로 설정할 수 있다.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        # detail/<int:pk>/
        return reverse('photo:detail', args=[self.id])