from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import SignUpForm, LoginForm
from .models import UserProfile
from chat.models import Message

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/home.html')

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='login')
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    all_users = UserProfile.objects.exclude(user=request.user)
    recent_messages = Message.objects.filter(
        sender=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'user_profile': user_profile,
        'all_users': all_users,
        'recent_messages': recent_messages,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')
