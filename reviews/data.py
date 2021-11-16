import pandas as pd
from . import my_globals
from django.conf import settings

def data_upload(file):
    df = pd.read_csv(file)
    df = df.rename(columns={
                    'Hora': 'DT',
                    'Nombre completo del usuario': 'Name',
                    'Usuario afectado': 'User_afec',
                    'Contexto del evento': 'Context',
                    'Componente': 'Component',
                    'Nombre evento': 'Event',
                    'Descripción': 'Description',
                    'Origen': 'Origen',
                    'Dirección IP': 'IP',
                })
    df = df.loc[df["Name"] != "-"]
    df = df.loc[df["Name"] != "Gestor General Cursos a Distancia"]
    df = descom_fecha(df)
    return df

def descom_fecha(df):
    # extraer fecha
    df['datefull'] = pd.to_datetime(df['DT'], format="%d/%m/%Y %H:%M", dayfirst=True)
    # Date
    df['date']= df['datefull'].dt.date
    df['year']= df['datefull'].dt.year
    df['month']= df['datefull'].dt.month
    df['day']= df['datefull'].dt.day
    # Time
    df['hour']= df['datefull'].dt.hour
    # Weekday
    df['wd'] = df['date'].map(lambda x: x.weekday())
    return df

def get_course_total_access(df):
    df2 = df['date'].value_counts().reset_index().rename(
            columns={'index': 'Date', 'date':'N'} ).sort_values('Date')
    return df2

def get_course_headmap(df):
    df2 = df[["wd","hour"]].value_counts().reset_index().rename(columns={0:'N'})
    return df2

def get_country_count_IP(df):
    import os
    import IP2Location

    database = IP2Location.IP2Location(os.path.join(settings.BASE_DIR, 'IP-COUNTRY.BIN'))
    df_ip = df['IP'].value_counts().reset_index().rename(
            #columns={'index': 'IP', 'Dirección IP':'N'})
            columns={'index': 'IP', 'IP':'N'})

    def find_country_from_ip(ip):
        rec = database.get_all(ip)
        return rec.country_long
    
    df_ip['Country'] = df_ip.apply(lambda x: find_country_from_ip(x['IP']), axis=1)
    df_ip2 = df_ip['Country'].value_counts().reset_index().rename(
            columns={'index': 'Country', 'Country':'N'})
     
    countries_codes_and_coordinates = pd.read_csv(os.path.join(settings.BASE_DIR, 'countries_codes_and_coordinates.csv'))
    countries_codes_and_coordinates3 = countries_codes_and_coordinates[['Country','Alpha-3 code']]
    
    df_ip2 = df_ip2.merge(countries_codes_and_coordinates3, how='left', on='Country')
    df_ip2['ISO'] =  df_ip2['Alpha-3 code'].str.replace('"','')
    df_ip2['ISO'] =  df_ip2['ISO'].str.replace(' ','')
    df_ip2 = df_ip2.dropna()
    
    return df_ip2