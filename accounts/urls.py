from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login, name='login-Page'),
    path('register/', views.register, name='Registeration-page'),
    path('logout/', views.logout, name='logout page'),
    path('verify/', views.verify, name='verification page'),
    path('re-password/', views.re_pass, name='forgot password'),
    path('username_verification/', views.re_pass_username, name='username verification')
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)