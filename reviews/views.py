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
from . import data, general, participants, cluster, my_globals
from .forms import NewUserForm

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
    # Construir nombres de los dataframes
    df_name =  request.session.session_key + "_df"
    dff_name = request.session.session_key + "_dff"
    new_df = bool(request.GET.get("new_df", False))

    # Si pinchó en eliminar datos
    if new_df:
        my_globals.DfC.pop(df_name)
        my_globals.DfC.pop(dff_name)
        return redirect('data_analysis')

    # "Si" está creado el df
    if df_name in my_globals.DfC.keys(): 
        df = my_globals.DfC[df_name]
        dff = my_globals.DfC[dff_name]
        if "date_s" in request.POST and "date_f" in request.POST: ## Filtrar
            # Capturar fechas en POST y guardarlas en session
            request.session['date_s'] = request.POST['date_s']
            request.session['date_f'] = request.POST['date_f']
            date_s= request.session['date_s']
            date_f= request.session['date_f']
            dff = df[ (df['datefull'] > pd.to_datetime(date_s)) & (df['datefull'] < pd.to_datetime(date_f)) ]
            my_globals.DfC[dff_name] = dff
            #dff = my_globals.DfC[dff_name]
            df2 = dff.head(10)
            df2_html = df2.to_html(classes="table table-striped table-sm", border=0)
            return render(request, 'data_analysis.html',
                {'result_present': True,
                    'df': df2_html,                    
                    'date_s': request.session['date_s'],
                    'date_f': request.session['date_f'],
                    'c_acc' : dff.shape[0]})
        df2 = dff.head(10)
        df2_html = df2.to_html(classes="table table-striped table-sm", border=0)
        return render(request, 'data_analysis.html',
            {'result_present': True,
                'df': df2_html,                    
                'date_s': request.session['date_s'],
                'date_f': request.session['date_f'],
                'c_acc' : dff.shape[0]})

    # No está creado el df
    if df_name not in my_globals.DfC.keys(): 
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            try:
                my_globals.DfC[df_name] = data.data_upload(myfile)
                my_globals.DfC[dff_name] = my_globals.DfC[df_name]
            except Exception:
                messages.error(request,"Algo pasó!")
            df = my_globals.DfC[df_name]  
            request.session['date_s'] = df["date"].min().strftime('%Y-%m-%d') 
            request.session['date_f'] = df["date"].max().strftime('%Y-%m-%d')   
            df2 = df.head(10)
            df2_html = df2.to_html(classes="table table-striped", border=0)
            return render(request, 'data_analysis.html',
                {'result_present': True,
                'df': df2_html,
                'date_s': request.session['date_s'],
                'date_f': request.session['date_f'],
                'c_acc' : df.shape[0]})
    # except Exception:
    #     messages.error(request,"No ha seleccionado fichero!")
    return render(request, 'data_analysis.html')

##### Análisis General basado en accesos  -------------------------------
@login_required
def general_analysis(request):
    dff_name = request.session.session_key + "_dff"
    if dff_name in my_globals.DfC.keys():
        div1 = general.plot_general_1(my_globals.DfC[dff_name])
        div2 = general.plot_general_heatmap(my_globals.DfC[dff_name])
        div3 = general.plot_act_acc(my_globals.DfC[dff_name])
        div4 = general.plot_act_acc2(my_globals.DfC[dff_name])
        div5 = general.plot_country_count_IP(my_globals.DfC[dff_name])
        return render(request, 'general.html',
                      {'result_present': True,
                       'div1': div1, 'div2': div2,
                       'div3': div3, 'div4': div4,
                       'div5': div5})
    return render(request,'general.html', {'result_present': False})

#####  Análisis de participantes  -------------------------------
@login_required
def part_analysis(request):
    dff_name = request.session.session_key + "_dff"
    if dff_name in my_globals.DfC.keys():
        ### Gráfico de cantidad de participantes por actividad
        div1 = participants.plot_part_act2(my_globals.DfC[dff_name])
        ### Agrupar usuariosmy_g
        df_usr_t1 = data.get_part_access(my_globals.DfC[dff_name])
        users_list = data.get_user_list(my_globals.DfC[dff_name])
        cant_part = df_usr_t1.shape
        ### Convertir df a html con pandas
        df_usr_t1_html = df_usr_t1.to_html(classes="table table-striped table-sm", border=0, justify="left")
        return render(request, 'participants.html',
                {'result_present': True,
                'div1': div1,
                #'div2': div2,
                'df': df_usr_t1_html, 'users_list': users_list,
                'cant_part': cant_part[0]})
    return render(request,'participants.html', {'result_present': False})

##### Análisis de actividades  -------------------------------
@login_required
def act_analysis(request):
    dff_name = request.session.session_key + "_dff"
    if dff_name in my_globals.DfC.keys():
        div1 = cluster.plot_act_acc(my_globals.DfC[dff_name])
        div2 = cluster.plot_act_acc2(my_globals.DfC[dff_name])
        return render(request, 'cluster.html',
                {'result_present': True,
                'div1': div1,
                'div2': div2
                #'df': df_usr_t1_html,'cant_part': cant_part[0]
                })
    return render(request,'cluster.html', {'result_present': False})