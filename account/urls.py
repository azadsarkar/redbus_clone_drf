from django.contrib import admin
from django.urls import path, include
from account import views
from .views import MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns =[
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('registration/',views.UserRegistrationAPI.as_view(), name = 'registration'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update/<int:pk>/', views.UserUpdateDeleteAPI.as_view(), name='user-update-delete'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_pass') 

]