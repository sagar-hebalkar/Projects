from django.urls import path
from django.urls.conf import include
from .views import *

urlpatterns = [
    path('', UserLogin.as_view()),
    path('login/',UserLogin.as_view(), name="login"),
    path('logout/',UserLogout.as_view(), name="logout"),
    path('sign-up/',UserSignUp.as_view(), name="sign_up"),
    path('setup-key/',SetupKey.as_view(), name="setup_key"),
    path('steganography/audio/encode/',AudioEncode.as_view(), name="encode"),
    path('steganography/audio/decode/',AudioDecode.as_view(), name="decode"),
]
