from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# My libs
import pandas as pd
from . import general, participants
import moodle_data.data
from core import my_globals

# Create your views here.


#### Cargar datos  PROFESOR -------------------------------
@login_required
def data_analysis(request):
    # Construir nombres de los dataframes
    df_name =  request.session.session_key + "_df"
    dff_name = request.session.session_key + "_dff"
    new_df = bool(request.GET.get("new_df", False))

    #Para cambio de mode a directivo
    if request.session['mode'] == "direct":
        if df_name in my_globals.DfC.keys(): 
            my_globals.DfC.pop(df_name)
            my_globals.DfC.pop(dff_name)
        request.session['mode'] = "prof"
        return render(request, 'data_analysis.html')

    # Si pinchó en eliminar datos
    if new_df:
        my_globals.DfC.pop(df_name)
        my_globals.DfC.pop(dff_name)
        return redirect('data_analysis')

    # "Si" está creado el df
    if df_name in my_globals.DfC.keys(): 
        df = my_globals.DfC[df_name]
        dff = my_globals.DfC[dff_name]
        if request.POST.getlist('multiple[]'):
            lista_usuarios_exclu = request.POST.getlist('multiple[]')
            my_globals.DfC[dff_name] = dff[~dff.Name.isin(lista_usuarios_exclu)]
        if "date_s" in request.POST and "date_f" in request.POST: ## Filtrar
            if request.POST['date_s'] > '' and request.POST['date_f'] > '':
                # Capturar fechas en POST y guardarlas en session
                request.session['date_s'] = request.POST['date_s']
                request.session['date_f'] = request.POST['date_f']
                date_s= request.session['date_s']
                date_f= request.session['date_f']
                dff = df[ (df['datefull'] > pd.to_datetime(date_s)) & (df['datefull'] <= pd.to_datetime(date_f)) ]
                my_globals.DfC[dff_name] = dff
        df2 = my_globals.DfC[dff_name].head(10)
        df2_html = df2.to_html(classes="table table-striped table-sm", border=0)
        users_list = moodle_data.data.get_user_list(my_globals.DfC[dff_name])
        return render(request, 'data_analysis.html',
            {'result_present': True,
                'df': df2_html, 'users_list': users_list,
                'date_s': request.session['date_s'],
                'date_f': request.session['date_f'],
                'c_acc' : len(my_globals.DfC[dff_name])})

    # No está creado el df
    if df_name not in my_globals.DfC.keys(): 
        if request.method == 'POST' and 'myfile1' in request.FILES:
            myfile1 = request.FILES['myfile1']
            #try:
            my_globals.DfC[df_name] = moodle_data.data.data_upload(myfile1)
            # if 'myfile2' in request.FILES:
            #     myfile2 = request.FILES['myfile2']
            #     my_globals.DfC[df_name] = moodle_backup.add_section_column(my_globals.DfC[df_name], myfile2)
            # else:
            #     myfile2 = ""
            my_globals.DfC[dff_name] = my_globals.DfC[df_name]
            # except Exception:
            #     messages.error(request,"Algo pasó!")
            df = my_globals.DfC[df_name]  
            request.session['date_s'] = df["date"].min().strftime('%Y-%m-%d') 
            request.session['date_f'] = df["date"].max().strftime('%Y-%m-%d')   
            df2 = df.head(10)
            df2_html = df2.to_html(classes="table table-striped", border=0)
            users_list = moodle_data.data.get_user_list(my_globals.DfC[dff_name])
            return render(request, 'data_analysis.html',
                {'result_present': True, 
                'df': df2_html, 'users_list': users_list,
                'date_s': request.session['date_s'],
                'date_f': request.session['date_f'],
                'c_acc' : df.shape[0]})
    # except Exception:
    #     messages.error(request,"No ha seleccionado fichero!")
    return render(request, 'data_analysis.html')

##### Análisis General basado en accesos  PROFESOR-------------------------------
@login_required
def general_analysis(request):
    dff_name = request.session.session_key + "_dff"
    if dff_name in my_globals.DfC.keys():
        div1 = general.plot_general_1(my_globals.DfC[dff_name])
        div2 = general.plot_general_heatmap(my_globals.DfC[dff_name])
        div3 = general.plot_act_acc(my_globals.DfC[dff_name])
        div4 = general.plot_act_acc2(my_globals.DfC[dff_name])
        div5 = general.plot_country_count_IP(my_globals.DfC[dff_name])
        cant_part = moodle_data.data.get_num_participants(my_globals.DfC[dff_name])
        cant_acc = len(my_globals.DfC[dff_name])
        cant_rec = moodle_data.data.get_num_resource(my_globals.DfC[dff_name])
        return render(request, 'general.html',
                      {'result_present': True,
                       'div1': div1, 'div2': div2,
                       'div3': div3, 'div4': div4, 'cant_acc': cant_acc, 'cant_rec': cant_rec,  
                       'div5': div5, 'cant_part': cant_part})
    return render(request,'general.html', {'result_present': False})

#####  Análisis de participantes  -------------------------------
@login_required
def part_analysis(request):
    dff_name = request.session.session_key + "_dff"
    if dff_name in my_globals.DfC.keys():
        ### Gráfico de cantidad de participantes por actividad
        div1 = participants.plot_part_act2(my_globals.DfC[dff_name])
        ### Agrupar usuariosmy_g
        df_usr_t1 = moodle_data.data.merge_part_df(my_globals.DfC[dff_name])
        try: 
            df_usr_cluster = moodle_data.data.create_df_cluster(df_usr_t1)
            div_usr_cluster = participants.plot_part_cluster(df_usr_cluster)
        except Exception:
            div_usr_cluster = "Se necesitan más de 2 participantes para el análisis de cluster"
        users_list = moodle_data.data.get_user_list(my_globals.DfC[dff_name])
        cant_part = moodle_data.data.get_num_participants(my_globals.DfC[dff_name])
        active_participation = moodle_data.data.get_num_active_participation(my_globals.DfC[dff_name])
        #cant_sesiones = data.get_num_session(my_globals.DfC[dff_name])
        cant_tareas_subidas = moodle_data.data.get_num_upload_assignments(my_globals.DfC[dff_name])
        ### Convertir df a html con pandas
        df_usr_t1_html = df_usr_t1.to_html(classes="table table-striped table-sm", border=0, justify="left")
        return render(request, 'participants.html',
                {'result_present': True,
                'div1': div1, 'div_usr_cluster':div_usr_cluster,
                #'div2': div2,
                'df': df_usr_t1_html, 'users_list': users_list, 'cant_tareas_subidas': cant_tareas_subidas,
                'cant_part': cant_part, 'active_participation': active_participation})
    return render(request,'participants.html', {'result_present': False})

##### Análisis de actividades  -------------------------------
# @login_required
# def act_analysis(request):
#     dff_name = request.session.session_key + "_dff"
#     if dff_name in my_globals.DfC.keys():
#         div1 = cluster.plot_act_acc(my_globals.DfC[dff_name])
#         div2 = cluster.plot_act_acc2(my_globals.DfC[dff_name])
#         return render(request, 'cluster.html',
#                 {'result_present': True,
#                 'div1': div1,
#                 'div2': div2
#                 #'df': df_usr_t1_html,'cant_part': cant_part[0]
#                 })
#     return render(request,'cluster.html', {'result_present': False})