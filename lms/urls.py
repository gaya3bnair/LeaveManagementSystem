from django.urls import path
from . import views
from django.contrib import admin
from django.conf import *
from django.conf.urls.static import static
urlpatterns = [
    path('', views.members_list, name='members'),
    path('leave', views.leave_request, name='requests'),
    path('user/<int:id>', views.user, name='user'),
    path('approve', views.approve, name='approve'),
    


] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
