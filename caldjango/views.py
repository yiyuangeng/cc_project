from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from calendarapp.forms import SigninForm
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm

def signin(request):
    forms = SigninForm()
    if request.method == 'POST':
        # print("ccc")
        forms = SigninForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            # print("aaa")
            if user:
                login(request, user)
                # print("bbb")
                return redirect('calendarapp:calendar')
    context = {'form': forms}
    return render(request, 'signin.html', context)

# def register(request):
#     return HttpResponse("register test")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password_1 = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password_1)
            login(request, user)
            return redirect('calendarapp:calendar')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('signin')