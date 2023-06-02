from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Follow, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'pk',
        'first_name',
        'last_name',
        'username',
        'email',
        'role',

    )
    search_fields = ('last_name', 'email')
    list_filter = ('last_name', 'email')
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author'
    )
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'
