from django import forms
from .models import Client


class UserForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('full_name', 'phone')
        labels = {
            'full_name': '',
            'phone': ''
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'consultation__form_input',
                                               'placeholder': "Введите Имя"}),
            'phone': forms.TextInput(attrs={'class': 'consultation__form_input',
                                            'placeholder': "+ 7 (999) 000 00 00"}),
        }
