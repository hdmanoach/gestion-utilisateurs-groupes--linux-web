"""
URL configuration for usermanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from manager import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.menu_view, name='menu'),
    path('menu/', views.menu_view, name='menu_view'),
    path('create_user/', views.create_user_view, name='create_user'),
    path('create_group/', views.create_group_view, name='create_group'),
    path('add_user_to_group/', views.add_user_to_group_view, name='add_user_to_group'),
    path('remove_user_from_group/', views.remove_user_from_group_view, name='remove_user_from_group'),
    path('delete_group/', views.delete_group_view, name='delete_group'),
    path('delete_user/', views.delete_user_view, name='delete_user'),
    path('show_user_groups/', views.show_user_groups_view, name='show_user_groups'),
    path('show_group_users/', views.show_group_users_view, name='show_group_users'),
    path('list_users/', views.list_users_search_view, name='list_users'),
    path('list_groups/', views.list_groups_view, name='list_groups'),
    path('add_user_to_group_sudo/',views.add_user_to_group_sudo,name='add_user_to_group_sudo'),
    path('logged_in_users/', views.logged_in_users_view, name='logged_in_users'),
    path('hystori_info/',views.hystori_info,name='hystori_info'),
    path('change_passwd/',views.change_passwd,name='change_passwd'),
    path('passwd_forget/',views.passwd_forget,name='passwd_forget'),
    path('view_logs_html/',views.view_logs_html,name='view_logs_html'),
    path('request_log_access/', views.request_log_access, name='request_log_access'),
    path('verify_log_code/', views.verify_log_code, name='verify_log_code'),
    path('resend_log_code/', views.resend_log_code, name='resend_log_code'),
    path('test-404/', views.test_404, name='test_404'),
]
