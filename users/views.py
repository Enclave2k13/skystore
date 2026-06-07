from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm
from .models import User


class RegisterView(CreateView):
    """Контроллер регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class UserLoginView(LoginView):
    """Контроллер авторизации пользователя"""
    authentication_form = UserLoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('catalog:home')


def logout_view(request):
    """Контроллер выхода из системы"""
    logout(request)
    return redirect('catalog:home')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('catalog:home')
    login_url = 'users:login'

    def get_object(self, queryset=None):
        return self.request.user