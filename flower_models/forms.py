from django import forms
from .models import Consultation

class UserForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ('name', 'phone')
        labels = {
            'name': '',
            'phone': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'consultation__form_input',
                                               'placeholder': "Введите Имя"}),
            'phone': forms.TextInput(attrs={'class': 'consultation__form_input',
                                            'placeholder': "+ 7 (999) 000 00 00"}),
        }
