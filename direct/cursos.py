from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

from core import my_globals
import moodle_data.data

def plot_top10_cursos_access(df):
        df_cursos = moodle_data.data.get_course_list_access(df)
        fig = px.line(df_cursos, x="Fecha", y="N", color="Curso")# ver 5 de plotly: markers=True
        fig.update_layout(showlegend=True)
        fig.update_layout(my_globals.BASE_LAYOUT)    
        # fig.update_layout({
        #                 "xaxis": {"title":"Componente principal 1"},
        #                 "yaxis": {"title":"Componente principal 2"},
        #                 "showlegend": True, 
        #                 'legend' : {"title":"Clusters"},
        #                 #'width': 900,
        #                 #'height': 500
        #                 })
        plot_div = plot(fig, output_type="div")
        return plot_div