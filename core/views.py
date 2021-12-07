from django.shortcuts import redirect, render
from django.http import HttpResponse

# Para auttenticación
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin

#from django.core.files.storage import FileSystemStorage
#from scipy import stats
from django.conf import settings
from django.contrib import messages

# My libs
import pandas as pd
from . import my_globals
from .forms import NewUserForm
import moodle_data.data
import subprocess

####### run shel para actuaizar aplicación  -------------- 

def update(request):
    if request.user.is_superuser:
        subprocess.call('/update_app.sh')
    else:
        error_message = 'No eres admin para ejecutar el script!'
    return render(request,'update.html',{})

####### login infrastructure  -------------- 
def logout_view(request):
    df_name =  request.session.session_key + "_df"
    dff_name = request.session.session_key + "_dff"
    if df_name in my_globals.DfC.keys(): 
        my_globals.DfC.pop(df_name)
        my_globals.DfC.pop(dff_name)
    logout(request)
    return redirect('login')

def login_view(request):
    error_message = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['mode'] = "prof"
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('index')
        else:
            error_message = 'Ups ... usuario o contraseña incorrectos!'
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'auth/login.html', context)

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="auth/register.html", context={"register_form":form})

####### END login infrastructure  -------------- 

### Home ---------------
def index(request):
    error_message = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['mode'] = "prof"
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('data_analysis')
        else:
            error_message = 'Ups ... usuario o contraseña incorrectos!'
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'index.html',context)

#### Ayuda   -------------------------------
def help(request):
    return render(request, 'help.html')

#### Destruir dataframes del dicionario global por petición del usuario -------------------------------
def del_global_df(request):
    df_name =  request.session.session_key + "_df"
    dff_name = request.session.session_key + "_dff"
    new_df = bool(request.GET.get("new_df", False))
    if new_df:
        my_globals.DfC.pop(df_name)
        my_globals.DfC.pop(dff_name)
    return render(request, 'index.html')
