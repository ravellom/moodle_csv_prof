from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

from core import my_globals
import moodle_data.data

def plot_part_act2(df):
        df4 = moodle_data.data.get_part_x_act(df)
        # start stop and step variables
        start, stop, step = 0, 43, 1
        df4["Context_br"] = df4.Contexto.str.slice(start, stop, step)
        df4['Context_br'] = df4.Context_br + "..."
        df4['Context_br'] = df4.Context_br.str.wrap(30)
        df4['Context_br'] = df4.Context_br.apply(lambda x: x.replace('\n', '<br>'))
        fig = px.bar(df4.head(10), y="Context_br", x='N')
        fig.update_layout(my_globals.BASE_LAYOUT)    
        fig.update_layout({     "xaxis": {  "title":"Cantidad de Estudiantes" },
                                "yaxis": {  "title":"Actividades"}
                                })
        plot_div = plot(fig, output_type="div")
        return plot_div

def plot_part_cluster(df):
        df['cluster'] = df['cluster'].map({0:'Grupo1', 1:'Grupo2'}) 
        df.loc[df.cluster == 1] = "Grupo2"
        fig = px.scatter(df, x='pca1', y='pca2', color='cluster', hover_data=["Usuario"])
                        #marginal_x='histogram', marginal_y='histogram',
                        #trendline="ols", template="simple_white", size=df_access3['N'])#, )
        fig.update_layout(my_globals.BASE_LAYOUT)    
        fig.update_layout({
                        "xaxis": {"title":"Componente principal 1"},
                        "yaxis": {"title":"Componente principal 2"},
                        "showlegend": True, 
                        'legend' : {"title":"Clusters"},
                        #'width': 900,
                        #'height': 500
                        })
        plot_div = plot(fig, output_type="div")
        return plot_div

