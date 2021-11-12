from django.shortcuts import redirect, render
#from django.http import HttpResponse

#from django.core.files.storage import FileSystemStorage
#from scipy import stats
from django.conf import settings
from django.contrib import messages

#import csv
import pandas as pd

# My libs
from . import my_globals
from . import data, general, participants, activities 


# Create your views here.

# Inicar dataframes
my_globals.DF = pd.DataFrame
my_globals.DFF = pd.DataFrame

def index(request):
    return render(request, 'index.html')

def help(request):
    return render(request, 'help.html')

#### Cargar datos   -------------------------------

def data_analysis(request):
    try:
        new_df = bool(request.GET.get("new_df", False))
        if new_df:
            my_globals.DF = my_globals.DF.iloc[0:0] # vaciar el df
            my_globals.DFF = my_globals.DFF.iloc[0:0]
            #new_df = False
            return redirect('data_analysis') #render(request, 'data_analysis.html')
        if my_globals.DF.empty:
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                my_globals.DF = data.data_upload(myfile)
                my_globals.DFF = my_globals.DF
                df2 = my_globals.DF.head(10)
                df2_html = df2.to_html(classes="table table-striped", border=0)
                return render(request, 'data_analysis.html',
                    {'result_present': True,
                    'df': df2_html,
                    'date_s': my_globals.DATE_S,
                    'date_f': my_globals.DATE_F,
                    'c_acc' : my_globals.DF.shape[0]})
        elif my_globals.DF.empty == False: 
            if "date_s" in request.POST and "date_f" in request.POST: ## Filtrar
                    my_globals.DATE_S = request.POST['date_s']
                    my_globals.DATE_F = request.POST['date_f']
                    my_globals.DFF = my_globals.DF[(my_globals.DF['datefull'] > my_globals.DATE_S) & (my_globals.DF['datefull'] < my_globals.DATE_F)]
            df2 = my_globals.DFF.head(10)
            df2_html = df2.to_html(classes="table table-striped table-sm", border=0)
            return render(request, 'data_analysis.html',
                {'result_present': True,
                    'df': df2_html,                    
                    'date_s': my_globals.DATE_S,
                    'date_f': my_globals.DATE_F,
                    'c_acc' : my_globals.DFF.shape[0]})
    except Exception:
        messages.error(request,"No ha seleccionado fichero!")
    return render(request, 'data_analysis.html')

##### Análisis General   -------------------------------

def general_analysis(request):
    if my_globals.DF.empty == False:
        div1 = general.plot_general_1(my_globals.DFF)
        div2 = general.plot_general_heatmap(my_globals.DFF)
        div3 = general.plot_country_count_IP(my_globals.DFF)
        return render(request, 'general.html',
                      {'result_present': True,
                       'div1': div1,
                       'div2': div2,
                       'div3': div3})
    return render(request,'general.html', {'result_present': False})

#####  Análisis de participantes  -------------------------------

def part_analysis(request):
    if my_globals.DF.empty == False:
        ### Gráfico de cantidad de participantes por actividad
        div1 = participants.plot_part_act2(my_globals.DFF)
        #div2 = participants.plot_general_heatmap(settings.DF, settings.DATE_S, settings.DATE_F)
        
        ### Agrupar usuarios
        df_usr_t1 = my_globals.DFF['Name'].value_counts().reset_index().rename(columns={'index': 'Usuario', 'Name':'Accesos'})
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

def act_analysis(request):
    if my_globals.DF.empty == False:

        ### hh
        div1 = activities.plot_act_acc(my_globals.DFF)
        div2 = activities.plot_act_acc2(my_globals.DFF)
        ### gg
   
        ### Convertir df a html con pandas
        #df_usr_t1_html = df_usr_t1.to_html(classes="table table-striped", border=0, justify="left")
        return render(request, 'activities.html',
                {'result_present': True,
                'div1': div1,
                'div2': div2
                #'df': df_usr_t1_html,'cant_part': cant_part[0]
                })

    return render(request,'activities.html', {'result_present': False})