from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

from . import my_globals


def plot_act_acc(df):
        df_comp = df['Component'].value_counts().reset_index().rename(
                        columns={'index': 'Component', 'Component':'N'})
        fig = px.pie(df_comp.head(8), values='N', names='Component',
                     hover_data=['Component'], labels={'N':'accesos'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        #fig = px.bar(df_comp, y="Component", x='N')
        fig.update_layout(my_globals.BASE_LAYOUT)
        # fig.update_layout({     "xaxis": {  "title":"Accesos" },
        #                         "yaxis": {  "title":"Tipos de Actividades"}
        #                         })
        plot_div = plot(fig, output_type="div")
        return plot_div

def plot_act_acc2(df):
        #df2 = df[df.Component.isin(["Foro", "Tarea", "Glosario","Cuestionario", "URL"])]
        df2 = df[df.Context.str.startswith(("Foro","Tarea","Glosario","Cuestionario", "URL"))]     
        df3 = ( df2[['Context']]
                .value_counts()
                .reset_index() 
                .rename(columns={'index': 'Context', 0:'N'}).sort_values(by='N') )
        start, stop, step = 0, 56, 1
        df3["Context_br"] = df3.Context.str.slice(start, stop, step)
        df3['Context_br'] = df3.Context_br.str.wrap(30)
        df3['Context_br'] = df3.Context_br.apply(lambda x: x.replace('\n', '<br>'))
        fig = px.bar(df3.head(10), y="Context_br", x='N')
        fig.update_layout(my_globals.BASE_LAYOUT)    
        fig.update_layout({     "xaxis": {  "title":"Accesos" },
                                "yaxis": {  "title":"Actividades"}
                                })
        plot_div = plot(fig, output_type="div")
        return plot_div
