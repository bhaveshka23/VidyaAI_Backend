from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views
from .views import SignUp,Login ,ProFile

#authentication API Endpoints

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #custome endpoints

    path('signup/' , SignUp.as_view() , name='signup'),
    path('login/' , Login.as_view() , name='login'),

    #profile api endpoint

    path('profile/<int:id>/' ,ProFile.as_view() , name='profile')

]
