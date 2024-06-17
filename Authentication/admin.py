from django.contrib import admin
from .models import User, notification, odpCode
# Register your models here.

admin.site.register(User)
admin.site.register(notification)
admin.site.register(odpCode)