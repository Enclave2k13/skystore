from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from catalog.mixins import BootstrapFormStylesMixin


class UserRegisterForm(BootstrapFormStylesMixin, UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'})
    )

    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        # Отправка приветственного письма
        self.send_welcome_email(user)
        return user

    def send_welcome_email(self, user):
        """Отправка приветственного письма пользователю"""
        subject = 'Добро пожаловать в Skystore!'
        message = f'''
        Здравствуйте!

        Спасибо за регистрацию в нашем интернет-магазине Skystore.
        Ваша учетная запись успешно создана.

        Теперь вы можете управлять товарами, добавлять новые продукты и многое другое.

        С уважением,
        Команда Skystore
        '''
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=True,
        )
        print(f"\n📧 Приветственное письмо отправлено на {user.email}\n")


class UserLoginForm(AuthenticationForm):
    """Форма авторизации пользователя"""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

class UserProfileForm(forms.ModelForm):
    """Форма редактирования профиля пользователя"""
    class Meta:
        model = User
        fields = ('avatar', 'phone', 'country')
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Страна'}),
        }