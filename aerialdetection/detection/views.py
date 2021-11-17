from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import detectAerialObjFromImage, detectAerialObjFromVideo
from django.conf import settings
from .forms import *
import os

class UserLogin(LoginView):
    template_name = 'detection/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("image_detection")
        return super().get(request, *args, **kwargs)

class UserSignUp(CreateView):
    template_name = 'detection/sign_up.html'
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('login')

class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")

class ImageDetection(LoginRequiredMixin,TemplateView):
    template_name = 'detection/image_detection.html'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        file = request.FILES["file"]
        input_path = os.path.join(settings.MEDIA_ROOT,"input_img",file.name)
        with open(input_path,"wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
            
        detection = detectAerialObjFromImage(input_path,file.name)
        kwargs["img_filename"] = file.name
        kwargs["detection"] = detection
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class VideoDetection(LoginRequiredMixin,TemplateView):
    template_name = 'detection/video_detection.html'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        file = request.FILES["file"]
        input_path = os.path.join(settings.MEDIA_ROOT,"input_video",file.name)
        with open(input_path,"wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
            
        detection = detectAerialObjFromVideo(input_path,file.name)
        print(detection)
        kwargs["video_filename"] = file.name
        kwargs["detection"] = detection
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class UnidentifiedImage(LoginRequiredMixin,TemplateView):
    template_name = 'detection/unidentified_img.html'
    login_url = reverse_lazy('login')
    extra_context = {}

    def get(self, request, *args, **kwargs):
        unidentified_img_dir =  os.path.join(settings.MEDIA_ROOT,"unidentified_img")
        unidentified_img_list = []
        for img in os.listdir(unidentified_img_dir):
            img_url = "/media/unidentified_img/"+img
            unidentified_img_list.append(img_url)
        
        self.extra_context["unidentified_img_url"] = unidentified_img_list
        return super().get(request, *args, **kwargs)