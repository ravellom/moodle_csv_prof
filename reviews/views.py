from django.shortcuts import redirect, render
#from django.http import HttpResponse

# Para auttenticación
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin

#from django.core.files.storage import FileSystemStorage
#from scipy import stats
from django.conf import settings
from django.contrib import messages

#import csv
import pandas as pd

# My libs
from . import my_globals
from . import data, general, participants, activities 

####### login infrastructure  -------------- 
def logout_view(request):
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

#### Cargar datos   -------------------------------
@login_required
def data_analysis(request):
    df_name =  request.session.session_key + "_df"
    dff_name = request.session.session_key + "_dff"
    if df_name in my_globals.DfC.keys():
        df = my_globals.DfC[df_name]
        dff = my_globals.DfC[dff_name]
    try:
        new_df = bool(request.GET.get("new_df", False))
        if new_df:
            my_globals.DfC[df_name] = my_globals.DfC[df_name].iloc[0:0]
            my_globals.DfC[dff_name] = my_globals.DfC[dff_name].iloc[0:0]
            return redirect('data_analysis') #render(request, 'data_analysis.html')
        if df_name not in my_globals.DfC.keys():
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                try:
                    my_globals.DfC[df_name] = data.data_upload(myfile)
                    my_globals.DfC[dff_name] = my_globals.DfC[df_name]
                except Exception:
                    messages.error(request,"Algo pasó!")
                df = my_globals.DfC[df_name]    
                df2 = df.head(10)
                df2_html = df2.to_html(classes="table table-striped", border=0)
                return render(request, 'data_analysis.html',
                    {'result_present': True,
                    'df': df2_html,
                    'date_s': my_globals.DATE_S,
                    'date_f': my_globals.DATE_F,
                    'c_acc' : df.shape[0]})
        elif df_name in my_globals.DfC.keys():
            if "date_s" in request.POST and "date_f" in request.POST: ## Filtrar
                    my_globals.DATE_S = request.POST['date_s']
                    my_globals.DATE_F = request.POST['date_f']
                    my_globals.DfC[dff_name] = df[df_name][(df['datefull'] > my_globals.DATE_S) & (df['datefull'] < my_globals.DATE_F)]
                    dff = my_globals.DfC[dff_name]
            df2 = dff.head(10)
            df2_html = df2.to_html(classes="table table-striped table-sm", border=0)
            return render(request, 'data_analysis.html',
                {'result_present': True,
                    'df': df2_html,                    
                    'date_s': my_globals.DATE_S,
                    'date_f': my_globals.DATE_F,
                    'c_acc' : dff.shape[0]})
    except Exception:
        messages.error(request,"No ha seleccionado fichero!")
    return render(request, 'data_analysis.html')

##### Análisis General   -------------------------------
@login_required
def general_analysis(request):
    dff_name = request.session.session_key + "_dff"
    if dff_name in my_globals.DfC.keys():
        div1 = general.plot_general_1(my_globals.DfC[dff_name])
        div2 = general.plot_general_heatmap(my_globals.DfC[dff_name])
        div3 = general.plot_country_count_IP(my_globals.DfC[dff_name])
        return render(request, 'general.html',
                      {'result_present': True,
                       'div1': div1,
                       'div2': div2,
                       'div3': div3})
    return render(request,'general.html', {'result_present': False})

#####  Análisis de participantes  -------------------------------
@login_required
def part_analysis(request):
    dff_name = request.session.session_key + "_dff"
    if dff_name in my_globals.DfC.keys():
        ### Gráfico de cantidad de participantes por actividad
        div1 = participants.plot_part_act2(my_globals.DfC[dff_name])
        ### Agrupar usuarios
        df_usr_t1 = my_globals.DfC[dff_name]['Name'].value_counts().reset_index().rename(columns={'index': 'Usuario', 'Name':'Accesos'})
        cant_part = df_usr_t1.shape
        ### Convertir df a html con pandas
        df_usr_t1_html = df_usr_t1.to_html(classes="table table-striped table-sm", border=0, justify="left")
        return render(request, 'participants.html',
                {'result_present': True,
                'div1': div1,
                #'div2': div2,
                'df': df_usr_t1_html,
                'cant_part': cant_part[0]})

    return render(request,'participants.html', {'result_present': False})

##### Análisis de actividades  -------------------------------
@login_required
def act_analysis(request):
    dff_name = request.session.session_key + "_dff"
    if dff_name in my_globals.DfC.keys():
        div1 = activities.plot_act_acc(my_globals.DfC[dff_name])
        div2 = activities.plot_act_acc2(my_globals.DfC[dff_name])
        return render(request, 'activities.html',
                {'result_present': True,
                'div1': div1,
                'div2': div2
                #'df': df_usr_t1_html,'cant_part': cant_part[0]
                })
    return render(request,'activities.html', {'result_present': False})