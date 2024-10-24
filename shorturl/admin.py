from django.contrib import admin
from .models import ShortURL, ClickLog
# Register your models here.

admin.site.register(ShortURL)
admin.site.register(ClickLog)
