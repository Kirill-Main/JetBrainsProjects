from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from shop.models import *


def login(request):
    context = {'error': ''}

    if request.user.is_authenticated:
        return HttpResponseRedirect(request.session['login_from'])

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(request.session['login_from'])
        else:
            context['error'] = 'Логин и/или пароль неправильные'
    else:
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')

    return render(request, 'registration/login.html', context)


def logout(request):
    auth.logout(request)
    if (referer := request.META.get('HTTP_REFERER', '/')) is not None:
        return HttpResponseRedirect(referer)
    return redirect("/")


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'registration/profile.html', {})


def register(request):
    context = {}

    if request.user.is_authenticated:
        return HttpResponseRedirect(request.session['register_from'])

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        if password != password2:
            context['error'] = 'Пароли не совпадают'
            return render(request, 'registration/register.html', context)

        user, created = User.objects.get_or_create(
            username=username)

        if created:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()
            auth.login(request, user)
            return redirect("/")
        else:
            context['error'] = 'Пользователь с таким именем уже существует'
    else:
        request.session['register_from'] = request.META.get('HTTP_REFERER', '/')

    return render(request, 'registration/register.html', context)

# Create your views here.
