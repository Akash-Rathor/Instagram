from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('<int:user_id>/company_dashboard/', views.dashboard, name='company dashboard'),all_customer
    path('company_dashboard/', views.dashboard, name='company dashboard'),
    path('post/', views.post, name='post'),
    path('menu/', views.my_menu, name='my menu'),
    path('add_customer/', views.add, name='new customer'),
    path('all_customer/', views.all_customer, name='all customer'),
    path('deleting_customer/<int:key_id>', views.delete_customer, name='delete customer'),
    path('<str:username>/', views.profile, name='profile'),
    path('add_follow/<str:username>',views.add_follow,name="add_follow"),
    path('del_follow/<str:username>',views.del_follow,name="del_follow"),
    path('like/<int:posts_id>',views.like_post,name="like"),
    path('unlike/<int:posts_id>',views.unlike_post,name="unlike"),
    path('followers/<str:username>',views.followers_page,name="followers_page"),
    path('following/<str:username>',views.following_page,name="following_page"),
    path('del/<str:username1>/<str:username>',views.remove_follower,name="remove_follower"),
    path('',views.infinite_post,name="infinite_post"),
    path('search/<str:username>',views.search_user,name="search_user"),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)