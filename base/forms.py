from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2', 'username']


class RoomForm(ModelForm):
    class Meta:
        model = rooms
        fields = '__all__'
        exclude = ['user', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields =[ 'name','avatar', 'username', 'email', 'bio']


