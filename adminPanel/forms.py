from django import forms
from application.models import *

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('product_img',)

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

class MetaInfoForm(forms.ModelForm):
    class Meta:
        model = MetaInfo
        fields = '__all__'