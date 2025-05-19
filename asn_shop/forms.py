from django import forms
from .models import MyUser, Car, CarImage, Review

class MyUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'phone_number', 'location', 'role', 'password']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['title', 'description', 'price', 'category', 'manufacturer']


class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

