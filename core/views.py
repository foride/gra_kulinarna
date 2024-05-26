from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard/')
        else:
            messages.error(request, 'email lub hasło jest nieprawdiłowe')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        if True:
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            password2 = request.POST['confirm-password']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Adres email już istnieje.')
                    return redirect('register')
                elif User.objects.filter(username=username).exists():
                    messages.error(request, 'Nazwa konta już istnieje')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    return redirect('login')
            else:
                messages.error(request, 'Hasła się różnią')
                return redirect('register')
    else:
        return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def about_view(request):
    return render(request, '')


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'dashboard.html')


def search_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'search.html')


def venue_details(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'venue details.html')


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'user profile.html')


def user_ranking(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'user ranking.html')


def achievements(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'achievements.html')
