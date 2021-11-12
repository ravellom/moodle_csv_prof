from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

from . import my_globals, data

def plot_general_1(df):
    course_total_access = data.get_course_total_access(df)
    fig = px.line(course_total_access, x="Date", y="N", template='plotly_white')
    fig.update_layout({ "xaxis": {  "title":"Fecha", 
                                    'type': 'date'},
                        "yaxis": {  "title":"Accesos"}
                        })
    access_mean = course_total_access.N.mean()
    fig.add_hline(y = access_mean, line_color = "red", line_width = 1, line_dash='dash')
    fig.update_layout(height=300)
    fig.update_layout(my_globals.BASE_LAYOUT)
    plot_div = plot(fig, output_type="div")#, config={"displayModeBar": False})
    return plot_div

def plot_general_heatmap(df):
    course_headmap = data.get_course_headmap(df)
    trace1 = go.Heatmap(
        z = course_headmap['N'],
        x = course_headmap['hour'],
        y = course_headmap['wd'], # zmin=-1, # zmax=1,
        xgap = 1, # Sets the horizontal gap (in pixels) between bricks
        ygap = 1,
        colorscale = 'blues' #'RdBu'
    )
    fig = go.Figure(data=trace1)
    fig.update_layout(height=300)
    fig.update_layout(my_globals.BASE_LAYOUT)
    fig.update_layout(  yaxis=dict( ticktext = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
                                    tickmode = 'array',
                                    tickvals = [0,1,2,3,4,5,6] ),
                        xaxis=dict( 
                                    tickmode = 'array',
                                    tickvals = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23] ))
                        
    plot_div = plot(fig, output_type="div", config={'responsive':True})#, config={"displayModeBar": False})
    return plot_div

def plot_country_count_IP(df):
    country_count_IP = data.get_country_count_IP(df)

    fig = px.choropleth(country_count_IP, locations="ISO",
                    color="N", # lifeExp is a column of gapminder
                    hover_name="Country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(height=300)
    fig.update_layout(my_globals.BASE_LAYOUT)
    plot_div = plot(fig, output_type="div")
    return plot_div
    
