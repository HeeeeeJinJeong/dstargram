from django.urls import path

from .views import *

app_name = 'photo'

urlpatterns = [
    path('create/', PhotoCreate.as_view(), name='create'),
    path('update/<int:pk>/', PhotoUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', PhotoDelete.as_view(), name='delete'),
    path('detail/<int:pk>/', PhotoDetail.as_view(), name='detail'),
    path('like/<int:photo_id>/', PhotoLike.as_view(), name='like'),
    path('like/', PhotoLikeList.as_view(), name='like_list'),
    path('save/', PhotoSaveList.as_view(), name='save_list'),
    path('save/<int:photo_id>/', PhotoSave.as_view(), name='save'),
    path('',PhotoList.as_view(), name='index'),
]