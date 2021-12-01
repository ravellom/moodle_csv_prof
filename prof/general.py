from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

from core import my_globals
import moodle_data.data

def plot_general_1(df):
    course_total_access = moodle_data.data.get_course_total_access(df)
    fig = px.line(course_total_access, x="Date", y="N", template='plotly_white')
    fig.update_layout({ "xaxis": {  "title":"Fecha", 
                                    'type': 'date'},
                        "yaxis": {  "title":"Accesos"}
                        })
    access_mean = course_total_access.N.mean()
    fig.data[0].update(mode='markers+lines')
    fig.add_hline(y = access_mean, line_color = "red", line_width = 1, line_dash='dash')
    fig.update_layout(height=400)
    fig.update_layout(my_globals.BASE_LAYOUT)
    plot_div = plot(fig, output_type="div", config={'responsive':True})#, config={"displayModeBar": False})
    return plot_div

def plot_general_heatmap(df):
    course_headmap = moodle_data.data.get_course_headmap(df)
    trace1 = go.Heatmap(
        z = course_headmap['N'],
        x = course_headmap['wd'],
        y = course_headmap['hour'], # zmin=-1, # zmax=1,
        xgap = 1, # Sets the horizontal gap (in pixels) between bricks
        ygap = 1,
        colorscale = 'blues', #'RdBu'
        colorbar=dict(thickness=5)
    )
    fig = go.Figure(data=trace1)
    fig.update_layout(my_globals.BASE_LAYOUT)
    fig.update_layout(  xaxis=dict( ticktext = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
                                    tickmode = 'array',
                                    tickvals = [0,1,2,3,4,5,6] ),
                        yaxis=dict( 
                                    ticktext = ['12am','2am','4am','6am','8am','10am',
                                                '12m','2pm','4pm','6pm', '8pm','10pm'],
                                    #ticktext = ['12am','1am','2am','3am','4am','5am','6am','7am','8am','9am','10am','11am',
                                     #           '12m','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm','9pm','10pm','11pm'],
                                    tickmode = 'array',
                                    #tickvals = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23] ))
                                    tickvals = [0,2,4,6,8,10,12,14,16,18,20,22] ))
    fig.update_layout(height=400)#,width=300)
    plot_div = plot(fig, output_type="div", config={'responsive':True})#, config={"displayModeBar": False})
    return plot_div

def plot_country_count_IP(df):
    country_count_IP = moodle_data.data.get_country_count_IP(df)
    fig = px.choropleth(country_count_IP, locations="ISO",
                    color="N", # lifeExp is a column of gapminder
                    hover_name="Country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
    #fig.update_layout(height=400)
    fig.update_layout(my_globals.BASE_LAYOUT)
    plot_div = plot(fig, output_type="div")
    return plot_div
    
def plot_act_acc(df):
        df_comp = moodle_data.data.get_comp_acc(df)
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
        df3 = moodle_data.data.get_act_acc(df)
        start, stop, step = 0, 43, 1
        df3["Context_br"] = df3.Context.str.slice(start, stop, step)
        df3['Context_br'] = df3.Context_br + "..."
        df3['Context_br'] = df3.Context_br.str.wrap(30)
        df3['Context_br'] = df3.Context_br.apply(lambda x: x.replace('\n', '<br>'))
        fig = px.bar(df3.head(10), y="Context_br", x='N')
        fig.update_layout(my_globals.BASE_LAYOUT)    
        fig.update_layout({     "xaxis": {  "title":"Accesos" },
                                "yaxis": {  "title":"Actividades"}
                                })
        plot_div = plot(fig, output_type="div")
        return plot_div

