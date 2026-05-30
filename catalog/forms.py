import re
from django.core.exceptions import ValidationError
from django import forms
from PIL import Image
import os
from .models import Product, Category

FORBIDDEN_WORD_ROOTS = [
    'казин',
    'крипт',
    'бирж',
    'дешев',
    'бесплатн',
    'обман',
    'полиц',
    'радар',
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название товара'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Выберите категорию"

        for field_name, field in self.fields.items():
            if isinstance(field.widget,
                          (forms.TextInput, forms.Textarea, forms.NumberInput, forms.Select, forms.ClearableFileInput)):
                field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})

    def _check_forbidden_words(self, value, field_name):
        """
        Проверка на запрещённые корни слов.
        Блокирует любые склонения: крипта, крипту, криптой, крипты и т.д.
        """
        if not value:
            return value

        value_lower = value.lower()

        for root in FORBIDDEN_WORD_ROOTS:
            # Ищем корень + любые буквы после (как маска крипт%)
            # \b - граница слова, чтобы не ловить часть другого слова
            pattern = r'\b' + re.escape(root) + r'\w*\b'

            if re.search(pattern, value_lower, re.UNICODE):
                raise forms.ValidationError(
                    f"Поле '{field_name}' содержит запрещённое слово (основа: '{root}'). "
                    f"Пожалуйста, удалите или замените его."
                )

        return value

    def clean_name(self):
        """Валидация названия"""
        name = self.cleaned_data.get('name')
        return self._check_forbidden_words(name, 'название')

    def clean_description(self):
        """Валидация описания"""
        description = self.cleaned_data.get('description')
        return self._check_forbidden_words(description, 'описание')

    def clean_price(self):
        """Валидация цены: не может быть отрицательной"""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError(
                "Цена не может быть отрицательной. Пожалуйста, введите корректную цену."
            )
        return price

    def clean_image(self):
        """Валидация изображения: формат, размер, корректность"""

        image = self.cleaned_data.get('image')
        if not image:
            return image

        if image.size > 5 * 1024 * 1024:
            raise ValidationError(
                f"Размер изображения не должен превышать 5 МБ. "
                f"Текущий размер: {image.size / (1024 * 1024):.1f} МБ."
            )

        ext = os.path.splitext(image.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            raise ValidationError(
                "Поддерживаются только форматы изображений: JPEG и PNG."
            )

        try:
            img = Image.open(image)
            if img.format not in ['JPEG', 'PNG']:
                raise ValidationError(
                    "Поддерживаются только форматы изображений: JPEG и PNG."
                )
        except Exception:
            raise ValidationError("Файл повреждён или не является корректным изображением.")

        image.seek(0)

        return image