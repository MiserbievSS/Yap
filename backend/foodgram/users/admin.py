from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
