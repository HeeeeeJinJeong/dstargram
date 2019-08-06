from django.shortcuts import render

# Create your views here.
# 유저 목록이 출력되는 뷰
# + follow 기능
# 중간 테이블을 직접 생성 - 모델

# 유저 모델 -> 유저 모델을 커스터마이징
# 확장하는 방법에 따라
# 1) 새로운 유저 모델을 만드는 방법 - 기존 유저 데이터를 유지할 수 없음
# 2) 기존 모델을 확장하는 방법 - DB 다운 타임 발 alter table - table lock

# 나를 팔로우 - 필드
# 내가 팔로우 - 필드

# 커스터마이징 불가할 경우
# 새로운 모델을 추가

# 사진 모델
# 사진을 좋아요 한 사람 - 필드
# 사진을 저장 한 사람 - 필드

"""
1. 유저 목록 or 유저 프로필에서 팔로우 버튼
1-1. 전체 유저 목록을 출력해주는 뷰 - 유저 모델에 대한 ListView
2. 팔로우 정보를 저장하는 뷰
"""

from .models import Follow

from django.views.generic.list import ListView
from django.contrib.auth.models import User


class UserList(ListView):
    model = User
    template_name = 'accounts/user_list.html'


class FollowerList(ListView):
    model = Follow
    template_name = 'accounts/follower_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = user.follower.all()
        return queryset

class FollowingList(ListView):
    model = Follow
    template_name = 'accounts/following_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = user.following.all()
        return queryset

from django.views.generic.base import View
from django.http import HttpResponseForbidden
from urllib.parse import urlparse
from django.http import HttpResponseRedirect

class Follow(View):
    def get(self, request, *args, **kwargs):

        # like를 할 정보가 있다면 진행, 없다면 중단
        if not request.user.is_authenticated:
            return HttpResponseForbidden
        else:
            if 'follow_id' in kwargs:
                follow_id = kwargs['follow_id']
                follow = Follow.objects.get(pk=follow_id)

                # 2) 누가?
                user = request.user
                if user in follow.me:
                    follow.me.remove(user)
                else:
                    follow.you.add(user)

            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path

            return HttpResponseRedirect(path)

# 기본에 입력받는 뷰는 CreateView 를 상속 -> 커스텀이 힘듦
# 회원가입 -> User 모델에 값을 입력받는다. -> CreateView
# 회원가입시 모델 필드 외에 추가 입력이 필요하다.
# 커스텀은 함수형 뷰가 적절
from django.contrib.auth.models import User
from .forms import SignUpForm

def signup(request):
    # class based view -> dispatch -> get, post
    if request.method == "POST":
        # form 이 채워져 있는 형태
        signup_form = SignUpForm(request.POST)

        # form validation
        if signup_form.is_valid():
            # 1. 저장하고 인스턴스 생성
            user_instance = signup_form.save(commit=False) # commit=False : DB 에는 저장 안됐으나 인스턴스는 생성
            # 2. 패스워드 암호화 -> 저장
            # form 이 가지고 있는 cleaned_data : 유효한 문자만 남긴 상태로, 처리 과정을 거친 데이터
            user_instance.set_password(signup_form.cleaned_data['password'])
            user_instance.save()

            return render(request, 'accounts/signup_complete.html', {'username':user_instance.username})
    else:
        signup_form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form':signup_form})

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount

def naver_signup(request, user, **kwargs):
    social_user = SocialAccount.objects.filter(user=user)

    if social_user.exists():
        user.last_name = social_user[0].extra_data['name']
        user.save()


# 시그널과 해당 함수를 connect
# 시그널 연결방법
# 1. receiver
# 2. connect
user_signed_up.connect(naver_signup)

from django.http import JsonResponse