from django.urls import path

from .views import *

app_name = 'photo'

urlpatterns = [
    path('create/', PhotoCreate.as_view(), name='create'),
    path('update/<int:pk>/', PhotoUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', PhotoDelete.as_view(), name='delete'),
    path('detail/<int:pk>/', PhotoDetail.as_view(), name='detail'),

    path('comment/create/<int:photo_id>/', comment_create, name='comment_create'),
    path('comment/update/<int:comment_id>/', comment_update, name='comment_update'),
    path('comment/delete/<int:comment_id>/', comment_delete, name='comment_delete'),

    path('like/<int:photo_id>/', PhotoLike.as_view(), name='like'),
    path('like/', PhotoLikeList.as_view(), name='like_list'),

    path('favorite/', PhotoSaveList.as_view(), name='favorite_list'),
    path('favorite/<int:photo_id>/', PhotoSave.as_view(), name='favorite'),

    path('mylist/', PhotoMyList.as_view(), name='mylist'),
    path('',PhotoList.as_view(), name='index'),
]