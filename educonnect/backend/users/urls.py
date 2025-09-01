from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    path('verify-email/<str:token>/', views.verify_email, name='verify-email'),
    path('reset-password/', views.password_reset_request, name='password-reset-request'),
    path('reset-password/<str:token>/', views.password_reset_confirm, name='password-reset-confirm'),
]