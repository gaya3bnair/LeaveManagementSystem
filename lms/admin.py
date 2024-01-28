from django.contrib import admin
from .models import Members, Leave
admin.site.register(Members)
# Register your models here.

admin.site.register(Leave)