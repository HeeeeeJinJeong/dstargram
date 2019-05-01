from django.contrib import admin

# Register your models here.
from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id','author','image','created','updated']
    list_filter = ['created','updated']
    search_fields = ['created','updated','text']
    ordering = ['-updated','-created']
    raw_id_fields = ['author']


admin.site.register(Photo, PhotoAdmin)