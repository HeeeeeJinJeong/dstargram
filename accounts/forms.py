# 모델 폼을 만들려면 2가지 필요
# (제네릭 뷰 : 제네릭 뷰, 모델)
# 모델 폼 : 모델, 폼

from django.contrib.auth.models import User
from django import forms

class SignUpForm(forms.ModelForm):
    # 작성 중 비밀번호 안보이게 하기, Meta보다 우선순위가 높음
    password = forms.CharField(label='Password', widget=forms.PasswordInput) # 우선순위가 높음
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        # fields 에는 해당 모델에 대해 입력받을 필드들을 나열한다.
        # 추가 필드도 포함될 수 있다. -> 필드 목록과 추가 필드가 겹치면 오버라이드 됨
        # fields 에 작성한 순서대로 출력한다.
        fields = ['username', 'password', 'password2', 'first_name', 'last_name', 'email'] # 입력 받을 내용
        # fields = '__all__' # 전부 입력 받을 때는 __all__

        # Todo : 필드의 기본 값, Placeholder 설정법, css Class 설정법, Validator 설정법, help text 설정법
        # Todo : 커스텀 필드 만드는 법

    # Repeat Password가 일치하지 않을 때
    # def clean_필드명(self):
    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        # 항상 필드의 값을 리턴한다.
        return cd['password2']