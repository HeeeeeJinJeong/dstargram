from django.contrib import admin

# Register your models here.
from .models import Follow

class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'me', 'you']
    raw_id_fields = ['me', 'you']

admin.site.register(Follow, FollowAdmin)