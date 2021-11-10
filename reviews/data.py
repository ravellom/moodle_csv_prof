import pandas as pd
from . import my_globals

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
    my_globals.DATE_S = pd.to_datetime(df["date"].min())
    my_globals.DATE_F = pd.to_datetime(df["date"].max())
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