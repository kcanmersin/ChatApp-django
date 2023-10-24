from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import ChatRoom,  Message, User, UserFollowing 
from .forms import ChatRoomForm, UserForm, MyUserCreationForm,UserProfileForm,MessageForm
from django.shortcuts import render, get_object_or_404
# Create your views here.
def home(request):
    return render(request,"base/home.html")

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})
@login_required
def follow(request, pk):
    user_to_follow = User.objects.get(id=pk)
    
    if request.user != user_to_follow:
        if not request.user.following.filter(following_user=user_to_follow).exists():
            UserFollowing.objects.create(user=request.user, following_user=user_to_follow)
    
    return redirect('user-profile', pk=user_to_follow.pk)
@login_required
def unfollow(request, pk):
    user_to_unfollow = User.objects.get(id=pk)
    
    if request.user.following.filter(following_user=user_to_unfollow).exists():
        request.user.following.filter(following_user=user_to_unfollow).delete()
    
    return redirect('user-profile', pk=user_to_unfollow.pk)
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    is_following = request.user.following.filter(following_user=user).exists()

    context = {'user': user,"is_following":is_following}
    return render(request, 'base/user-profile.html', context)
def searchPage(request):
    query = request.GET.get('q')

    if query:
        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(name__icontains=query)
        )
    else:
        results = User.objects.none()  # No results when the search query is empty
    result_count = len(results)
    print(result_count)
    print(results)
    context = {'results': results , "result_count":result_count}
    return render(request, 'base/search.html', context)


@login_required
def editProfilePage(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=request.user.id)  # Profil sayfasına yönlendirme yapabilirsiniz
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'base/edit-profile.html', context)

def chatPage(request, pk):
    current_user = request.user
    profile_user = get_object_or_404(User, pk=pk)
    chat_room = ChatRoom.objects.filter(members=current_user).filter(members=profile_user).first()

    if chat_room is None:
        chat_room = ChatRoom.objects.create(name="Sohbet Odası Adı")
        chat_room.members.add(current_user, profile_user)

    if request.method == 'POST':
        form = MessageForm(request.POST)  # Replace with your actual form class
        if form.is_valid():
            message_text = form.cleaned_data['body']
            message = Message(user=current_user, chatroom=chat_room, body=message_text)
            message.save()
            # Redirect to the same chat page to clear the form
            return redirect('chat-room', pk=pk)
    else:
        form = MessageForm()  # Replace with your actual form class

    messages = Message.objects.filter(chatroom=chat_room).order_by('-created')[:8]
    messages = reversed(messages)


    context = {
        'chat_room': chat_room,
        'profile_user': profile_user,
        'current_user': current_user,
        'messages': messages,
        'form': form  # Pass the form to the template
    }

    return render(request, 'base/chat-room.html', context)
def groupChatPage(request,pk):

    pass