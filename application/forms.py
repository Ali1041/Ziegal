from django import forms
from .models import *

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = '__all__'