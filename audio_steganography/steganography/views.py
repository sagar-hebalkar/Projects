from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import encodeAudio, decodeAudio
import rsa
from .forms import *
from .models import *

class UserLogin(LoginView):
    template_name = 'steganography/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("encode")
        return super().get(request, *args, **kwargs)

class UserSignUp(CreateView):
    template_name = 'steganography/sign_up.html'
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('login')

class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


class SetupKey(LoginRequiredMixin,TemplateView):
    template_name = 'steganography/setup_key.html'
    login_url = reverse_lazy('login')
    extra_context = {}

    def get(self, request, *args, **kwargs):
        key_pair = RSAKeyPair.objects.filter(user=request.user)
        if key_pair:
            self.extra_context["public_key"] = key_pair.first().public_key
            self.extra_context["private_key"] = key_pair.first().private_key
        else:
            self.extra_context["public_key"] = "Key has not generated yet"
            self.extra_context["private_key"] = "Key has not generated yet"
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        (pubkey, privkey) = rsa.newkeys(1208)
        key_pair = RSAKeyPair.objects.filter(user=request.user)
        if key_pair:
            key_pair = key_pair.first()
        else:
            key_pair = RSAKeyPair() 
            key_pair.user = request.user
        key_pair.public_key = f"{pubkey.n},{pubkey.e}"
        key_pair.private_key = f"{privkey.n},{privkey.e},{privkey.d},{privkey.p},{privkey.q}"
        key_pair.save()
        return redirect("setup_key")


class AudioEncode(LoginRequiredMixin,TemplateView):
    template_name = 'steganography/audio_encode.html'
    login_url = reverse_lazy('login')
    
    def post(self, request, *args, **kwargs):
        audio_file = request.FILES["audio_file"]
        secret_text = request.POST["secret_text"].strip()
        public_key = request.POST["public_key"]
        
        op_filename = encodeAudio(audio_file,secret_text,public_key)
        kwargs["output_path"] = op_filename
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class AudioDecode(LoginRequiredMixin,TemplateView):
    template_name = 'steganography/audio_decode.html'
    login_url = reverse_lazy('login')
    extra_context = {}

    def get(self, request, *args, **kwargs):
        key_pair = RSAKeyPair.objects.filter(user=request.user)
        if not key_pair:
            return redirect("setup_key")
        self.extra_context["private_key"] = key_pair.first().private_key
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES["audio_file"]
        private_key = request.POST["private_key"]
        
        secret_text = decodeAudio(audio_file,private_key)
        kwargs["secret_text"] = secret_text
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)