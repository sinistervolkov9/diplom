from django.urls import path
from .apps import UsersConfig
from .views import RegisterView, VerifyCodeView
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
]
