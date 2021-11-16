from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

from . import my_globals

def plot_part_act2(df):
        #df2 = df[df.Component.isin(["Foro", "Tarea", "Glosario","Cuestionario", "URL"])]
        df2 = df[df.Context.str.startswith(("Foro","Tarea","Glosario","Cuestionario", "URL"))]     
        df3 = ( df2[['Context','Name']]
                .value_counts()
                .reset_index() 
                .rename(columns={'index': 'Contexto', 0:'N'}) )
        df4 = ( df3[['Context']]
                .value_counts()
                .reset_index() 
                .rename(columns={'Context': 'Contexto', 0:'N'}).sort_values(by='N') )
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

