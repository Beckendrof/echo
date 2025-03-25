from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User, Creator, Editor

def login(request):
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        user = User(
            user_type = request.POST['user_type'],
            email = request.POST['email'],
            password = request.POST['password']
        )
        user.save()

        if user.user_type == 'creator':
            creator = Creator(
                user = user,
                youtube_channel = request.POST['youtube_channel'],
                brand_name = request.POST['brand_name']
            )
            creator.save
        else:
            editor = Editor(
                user = user,
                display_name = request.POST['display_name']
            )
            editor.save()
        return redirect('login')
    else:
        form = UserRegistrationForm()
        return render(request, 'home.html', {'form': form})

def home(request):
    form = UserRegistrationForm()
    users = User.objects.all()
    context = {
        'form': form,
        'users': users
    }
    return render(request, 'home.html', context)
