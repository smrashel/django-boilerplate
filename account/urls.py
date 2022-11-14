from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('users/', views.users, name="users"),
    path('users/create/', views.user_create, name="user_create"),
    path('users/<str:pk>/update/', views.user_update, name="user_update"),
    path('users/<str:pk>/delete/', views.user_delete, name="user_delete"),
    path('users/change-password/', views.change_password, name="change_password"),

    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='account/password/password_reset.html'), name="password_reset"),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='account/password/password_reset_done.html'), name="password_reset_done"),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='account/password/password_reset_complete.html'), name="password_reset_complete"),

]