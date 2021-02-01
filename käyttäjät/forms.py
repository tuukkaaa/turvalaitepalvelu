from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


from .models import *

class AsiakasLomake(ModelForm):
    class Meta:
        model = Asiakas
        fields = '__all__'
        exclude = ['käyttäjä']


class TilausLomake(ModelForm):
    class Meta:
        model = Tilaus
        fields = '__all__'



class LuoKäyttäjäLomake(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

