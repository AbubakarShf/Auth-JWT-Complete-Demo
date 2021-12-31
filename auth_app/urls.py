from django.urls import path
from .views import StudentData,Register,Logout,Login
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
urlpatterns = [
    path('student',StudentData.as_view(),name="view data"),
    path('login',Login.as_view(),name="login"),
    path('logout',Logout.as_view(),name="logout"),
    path('register',Register.as_view(),name="Register"),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify', TokenVerifyView.as_view(), name='token_verify')
]
