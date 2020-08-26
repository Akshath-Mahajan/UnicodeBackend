from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import customAuthenticationForm, customSignupForm
class Login(LoginView):
    template_name = 'Accounts/login.html'
    authentication_form = customAuthenticationForm
class Signup(CreateView):
    form_class = customSignupForm
    success_url = reverse_lazy('login')
    template_name = 'Accounts/signup.html'

class Profile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Accounts/profile.html')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')