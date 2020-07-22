from django.shortcuts import render, redirect
from login.models import *
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def new_user(request):
    return render(request, 'new_user.html')

def edit_self(request):
    context = {
        'self' : User.objects.filter(email = request.session['logged_user']).all().first()
    }
    return render(request, 'edit_user.html', context)

def update_info(request):
    if request.method == "POST":
        errors = User.objects.edit_info_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/edit')
        else:
            user = User.objects.filter(email = request.POST['user']).all().first()
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            if 'user_level' in request.POST:
                user.user_level = request.POST['user_level']
            user.save()
            request.session['logged_user'] = request.POST['email']
            return redirect('/dashboard')
    else:
        return redirect('/users/edit')

def update_pw(request):
    if request.method == "POST":
        errors = User.objects.edit_password_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/edit')
        else:
            user = User.objects.filter(email = request.session['logged_user']).all().first()
            password = request.POST['new_password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user.password = pw_hash
            user.save()
            return redirect('/dashboard')
    else:
        return redirect('/users/edit')

def update_desc(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['user']).all().first()
        user.desc = request.POST['desc']
        user.save()
        return redirect('/dashboard')
    else:
        return redirect('/users/edit')

def edit_user(request, num):
    user = User.objects.filter(email = request.session['logged_user']).all().first()
    if user.user_level != 9:
        return redirect('/users/edit')
    else: 
        context = {
            'self' : User.objects.get(id = num),
            'current_user':user
        }
        return render(request, 'edit_user.html', context)

def show_user(request, num):
    context = {
        'user':User.objects.get(id = num)
    }
    return render(request, 'show_user.html', context)

def post(request, num):
    Post.objects.create(content = request.POST['post'], receiver = User.objects.get(id = num), poster = User.objects.filter(email = request.session['logged_user']).all().first())
    return redirect('/users/show/{}'.format(num))
def comment(request, num, num1):
    Comment.objects.create(content = request.POST['comment'], user = User.objects.filter(email = request.session['logged_user']).all().first(), post = Post.objects.get(id = num1))
    return redirect('/users/show/{}'.format(num))