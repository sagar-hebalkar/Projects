from django.urls import path
from .views import *

urlpatterns = [
    path('', UserLogin.as_view()),
    path('login/',UserLogin.as_view(), name="login"),
    path('logout/',UserLogout.as_view(), name="logout"),
    path('sign-up/',UserSignUp.as_view(), name="sign_up"),
    path('detetction/image/',ImageDetection.as_view(), name="image_detection"),
    path('detetction/video/',VideoDetection.as_view(), name="video_detection"),
    path('unidentified/image/',UnidentifiedImage.as_view(), name="unidentified_img"),
]