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