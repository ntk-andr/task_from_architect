from django.urls import path, include
from users.views import (
    IndexView, RegistrationUserView, LoginUserView, DetailUserView, DeleteUserView, LogoutUserView, ProfileUserView,
    UserPasswordChangeView, UserPasswordChangeDoneView, UserPasswordResetView, EmailVerificationView
    )

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    path('<uuid:id>/profile/', ProfileUserView.as_view(), name='profile'),
    path('<id>/delete/', DeleteUserView.as_view(), name='delete'),
    path('<id>/', DetailUserView.as_view(), name='info'),

    path('register', RegistrationUserView.as_view(), name='register'),
    path('login', LoginUserView.as_view(), name='login'),
    path('logout', LogoutUserView.as_view(), name='logout'),
    
    path('password_change', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done', UserPasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path('password_reset', UserPasswordResetView.as_view(), name='password_reset'),
    path('verify/<str:email>/<code>/', EmailVerificationView.as_view(), name='email_verification'),
]
