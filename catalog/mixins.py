from typing import Any
from django import forms


class BootstrapFormStylesMixin:
    """Миксин для автоматической стилизации форм Bootstrap"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            existing_class = field.widget.attrs.get('class', '')

            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = f'form-select {existing_class}'.strip()
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = f'form-check-input {existing_class}'.strip()
            else:
                field.widget.attrs['class'] = f'form-control {existing_class}'.strip()