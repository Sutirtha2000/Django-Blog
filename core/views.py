from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import RegistrationForm, LoginForm
# Create your views here.

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        
        form = LoginForm()
        next_url = request.GET.get('next')
        print(next_url)

        context = {
            'form' : form,
            'next' : next_url
        }
        return render(request, 'core/login.html',context=context)
    
    def post(self, request):
        form = LoginForm(request, request.POST)
        next_url = request.POST.get('next')
        print(next_url)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user=user)
                messages.success(request, "You are logged in successfully!")
                # next_url = request.GET.get('next', 'home')
                if next_url and next_url != "None" and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    # print(next_url)
                    return redirect(next_url)
                # if next_url == "None":
                #     print(next_url)
                #     return redirect('home')
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
        else:
            context = {
                'form' : form,
                'next' : next_url
            }
            return render(request, 'core/login.html', context=context)


class RegisterView(View):
    def get(self, request):
        context = {
            'form' : RegistrationForm()
        }
        return render(request, 'core/register.html', context=context)
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(username=username, password=password)
            # user.set_password(password)
            # user.save()
            # user = form.save()
            login(request, user=user)
            messages.success(request, "You are registered successfully !!!")
            return redirect('home')
        else:
            context = {'form' : form}
            return render(request, 'core/register.html', context=context)


class LogoutView(View):
    def post(self, request):
        next_url = request.POST.get('next')
        # print(next_url)
        logout(request)
        messages.success(request, "You are Logged out Successfully !!!")
        # next_url = request.GET.get('next', 'home')
        if next_url:
            return redirect(next_url)
        return redirect('home')