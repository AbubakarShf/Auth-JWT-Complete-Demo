from django.urls import path
from .views import StudentData,Register,Logout,Login
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('student',StudentData.as_view(),name="view data"),
    path('login',Login.as_view(),name="login"),
    path('logout',Logout.as_view(),name="logout"),
    path('register',Register.as_view(),name="Register"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
