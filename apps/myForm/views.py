from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from .models import User, Creator, Editor

def login(request):
    form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'login.html', context)

def login_success(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=email, password=password)
        if user:
            print('User found')
            return redirect('home')
    return login(request)

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
    user = User.objects.all()
    context = {
        'form': form,
        'user': user
    }
    return render(request, 'home.html', context)
