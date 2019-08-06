from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import UserList, signup, FollowerList, FollowingList, Follow

app_name = 'accounts'

urlpatterns = [
    path('user/list/', UserList.as_view(), name='user_list'),
    path('signin/', LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('signout/', LogoutView.as_view(template_name='accounts/signout.html'), name='signout'),
    path('signup/', signup, name='signup'),
    path('follower_list/', FollowerList.as_view(), name='follower_list'),
    path('following_list/', FollowingList.as_view(), name='following_list'),
    path('follow/<int:follow_id>/', Follow.as_view(), name='follow'),
]