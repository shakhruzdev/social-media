from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import MyUser


def login_view(request):
    context = {}
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            context['error'] = 'User with this username does not exists'
    return render(request, 'signin.html', context=context)


@login_required(login_url='auth/signin/')
def logout_view(request):
    logout(request)
    return redirect('/auth/login')


def register_view(request):
    context = {}
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        p1 = data['password1']
        p2 = data['password2']
        if not User.objects.filter(username=username).exists() and p1 == p2:
            user = User.objects.create(username=username, password=make_password(p1))
            user.save()
            my_user = MyUser.objects.create(user=user)
            my_user.save()
            return redirect('/auth/login')
        context['error'] = 'User with this username already exists or passwords did not match'
    return render(request, 'signup.html', context=context)
