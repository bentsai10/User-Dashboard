from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def process_login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        else:
            request.session['logged_user'] = request.POST['email']
            return redirect('/dashboard')
    else:
        if 'logged_user' not in request.session:
            return redirect('/login')
        else:
            return redirect('/dashboard')


def login(request):
    return render(request, 'sign_in.html')

def process_register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            if User.objects.all().count() == 0:
                admin_level = 9
            else:
                admin_level = 1
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], user_level = admin_level, password = pw_hash)
            request.session['logged_user'] = request.POST['email']
            return redirect('/dashboard')
    else:
        if 'logged_user' not in request.session:
            return redirect('/login')
        else:
            return redirect('/dashboard')

def register(request):
    return render(request, 'register.html')

def dashboard(request):
    context = {
        'current_user': User.objects.filter(email = request.session['logged_user']).all().first(),
        'users' : User.objects.all()
    }
    return render(request, 'dashboard.html', context)

def dash_admin(request):
    pass

def logout(request):
    if 'logged_user' in request.session:
        del request.session["logged_user"]
    return redirect('/')