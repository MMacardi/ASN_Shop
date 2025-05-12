from django import forms
from .models import MyUser, Car, CarImage

class MyUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'phone_number', 'location', 'role', 'password']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['title', 'description', 'price', 'category']


class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image']

