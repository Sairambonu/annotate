from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm, CustomUserAuthenticationForm
from .models import UserLoginInfo
from annotate.models import AnnotateLanguageUsers
from django.core import serializers
import datetime
from time import gmtime, strftime


def index_page(request):
    return redirect(user_login)

def user_login(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Assuming you have a Users model that represents the phpMyAdmin users table
        try:
            user = UserLoginInfo.objects.get(username=username)
        except UserLoginInfo.DoesNotExist:
            user = None
        
        if user is not None and user.check_password(password):
            if user.status=='active':
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('annotates')
            else:
                context['error'] = 'Your account is inactive. Please contact the coordinator'
        else:
            context['error'] = 'Invalid username or password.'
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            languages = form.cleaned_data.get('languages',[])
            email = form.cleaned_data.get('email')
            # for lang in languages:
            #     AnnotateLanguageUsers.objects.create(email=email,lang=lang)
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='/login/')
def profile_view(request):
    return render(request, 'profile.html')


@login_required(login_url='/login/')
def profile_edit(request):
    context={}

    if request.method=='POST':
        usercontact= request.POST.get('usercontact')

        if hasattr(request,"user"):
            username= request.user.username
        else:
            context['error'] = 'user session expired'

        if username is not None:
            user = UserLoginInfo.objects.get(username=username)
            user.phone = usercontact
            user.save()
            messages.success(request, 'phone no changed successfully')
            return redirect('profile')
        else:
            context['error'] = 'user DoesNotExist'

    
    return render(request, 'edit_profile.html', context)


@login_required(login_url='/login/')
def change_password(request):
    context = {'error': ''}

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        username = None
        if hasattr(request, "user"):
            username = request.user.username
        else:
            context['error'] = context.get('error', '') + "User session expired.!"
        
        if username is not None:
            if(request.user.password==old_password):
                if(new_password==confirm_password):
                    try:
                        user = UserLoginInfo.objects.get(username=username)
                        user.password = new_password
                        user.save()
                        messages.success(request, 'Password Updated...!')
                        context['success'] = context.get('success', '') + "Password Updated...!"
                    
                    except UserLoginInfo.DoesNotExist:
                        context['error'] = 'User Does not exists...!'
                    
                else:
                    context['error'] = context.get('error', '') + "Password mismatch.!"
            else:
                context['error'] = context.get('error', '') + "Old Password don't match.!"
    
    return render(request, 'change_password.html', context)


@login_required(login_url='/login/')
def manage_users(request):
    user_email = None
    if hasattr(request, "user"):
        user_email = request.user.email
    else:
        messages.info(request, "User session expired.!")
    
    users = []
    if user_email is not None:
        object_list = serializers.serialize("python", UserLoginInfo.objects.all())

        for object in object_list:
            entry = object.get('fields', {})
            entry['username'] = object.get('pk', '')
            users.append(entry)
    
    return render(request, 'manage_users.html', {'users': users})

def act_deact(request,username):
    username = str(username)
    user = UserLoginInfo.objects.get(username=username)
    if user.status=='active':
        user.status='deactive'
    else:
        user.status='active'
    user.save()
    return redirect('manage_users')

def contact(request):
    return render(request, 'contact.html')
def endpoint(request):
    return render(request,'endpoint.html')

@login_required(login_url='/login/')
def custom_logout(request):
    logout(request)
    return redirect('login')



