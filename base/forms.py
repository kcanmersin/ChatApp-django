from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import ChatRoom, User,Message


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class ChatRoomForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'bio', 'avatar']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']