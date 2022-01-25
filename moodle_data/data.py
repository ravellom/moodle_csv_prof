# Módulo de creación y consultas al dataframe a partir de un Reporte de Moodle
# Autor: Raidell Avello, Universidad de Cienfuegos
###

import pandas as pd
#from . import my_globals
from django.conf import settings
import os
#from glob import iglob
import IP2Location
from . import moodle_backup, cluster

# VARIABLES GLOBALES ·········

# Eventos de participación activa
ACTIVE_PART = [
    # Foro
    "Algún contenido ha sido publicado.", "Tema creado", "Mensaje creado", "Mensaje actualizado",
    # Tarea
    "Se ha enviado una entrega", "Se ha entregado una extensión",
    # Wiki
    "Comentario creado", "Página wiki creada", "Página de la wiki actualizada",
    # Taller
    "Se ha subido una entrega", "Entrega creada", "Entrega actualizada",
    # Cuestionario
    "Intento enviado",
    # Glosario y Comentarios
    "Comentario creado",
    # Glosario
    "La entrada ha sido creada", "La entrada ha sido actualizada"
    # Chat
    "Mensaje enviado",
    # Módulo de encuesta
    "Respuesta enviada"]

ACTIVE_PART_FORO = [
    "Algún contenido ha sido publicado.", "Tema creado", "Mensaje creado", "Mensaje actualizado"]

COMPLETED_ASSIGMENT = "Se ha enviado una entrega"

GLOSARY_PART = [    
    # Glosario
    "Comentario creado", "La entrada ha sido creada", "La entrada ha sido actualizada"]

CUESTIONARIO_PART = ["Intento enviado"]

# ·········


# CREACIÓN DEL DATAFRAME ·········

def data_upload(file):
    df = pd.read_csv(file)
    df = change_columns_name(df)
    df = del_user_by_name(df, ["-"])
    df = add_mont_day_hour_columns(df)
    df = add_weekday_columns(df)
    df = add_ID_user_column(df)
    df = add_ID_resource_column(df)
    #df = create_dynamic_session_id(df)
    #df = moodle_backup.course_structure(df, backup_file)
    return df

def df_from_multiple_file(files):
    df = pd.DataFrame()
    for f in files:
        dfaux = data_upload(f)
        #pos1 = f.find("\\")
        pos2 = str(f.name).find(".csv")
        nombre_curso = str(f.name)[0:pos2]
        dfaux["Curso"] = nombre_curso
        df = pd.concat([df,dfaux], ignore_index=True)
    return df

def change_columns_name(df):
    df = df.rename(columns={
        'Hora': 'DT',
        'Nombre completo del usuario': 'Name',
        'Usuario afectado': 'User_afec',
        'Contexto del evento': 'Context',
        'Componente': 'Component',
        'Nombre evento': 'Event',
        'Nombre del evento': 'Event', # para otros formato
        'Descripción': 'Description',
        'Origen': 'Origen',
        'Dirección IP': 'IP',
    })
    return df


def add_mont_day_hour_columns(df):
    # extraer fecha
    try:
        df['datefull'] = pd.to_datetime(
            df['DT'], format="%d/%m/%Y %H:%M", dayfirst=True)
    except:
        df['datefull'] = pd.to_datetime(
            df['DT'], dayfirst=True)
    # Date
    df['date'] = df['datefull'].dt.date
    df['year'] = df['datefull'].dt.year
    df['month'] = df['datefull'].dt.month
    df['day'] = df['datefull'].dt.day
    # Time
    df['hour'] = df['datefull'].dt.hour
    return df


def add_weekday_columns(df):
    # Weekday
    df['wd'] = df['datefull'].dt.weekday
    #df['wd'] = df['date'].map(lambda x: x.weekday())
    return df


def add_ID_user_column(df) -> pd.DataFrame:
    df["ID_Usuario"] = df["Description"].str.extract(
        '[i][d]\s\'(\d*)\'', expand=True)
    return df


def add_ID_resource_column(df) -> pd.DataFrame:
    df["ID_Recurso"] = df["Description"].str.extract(
        'with course module id\s\'(\d*)\'\.', expand=True)
    df["ID_Recurso"] = pd.to_numeric(df["ID_Recurso"])
    return df


def create_dynamic_session_id(df) -> pd.DataFrame:
    # Crea un identificador para distinguir la sesión a la que pertenece cada evento en función de un tiempo
    # umbral que sirva para aproximarlas.
    THRESHOLD = 1800
    result = df.sort_values(by=['ID_Usuario', 'date'])
    previous_row = None
    sessionids = [None] * len(result)
    user_session_counter = 0
    session_counter = 0
    for index, row in result.iterrows():
        if previous_row is not None:
            if row['ID_Usuario'] != previous_row['ID_Usuario']:
                user_session_counter = 0
            distance = row['date'] - previous_row['date']
            if distance.total_seconds() > THRESHOLD:
                user_session_counter += 1
        sessionid = "{}:{}".format(row['ID_Usuario'], user_session_counter)
        sessionids[session_counter] = sessionid
        session_counter += 1
        previous_row = row
        result['ID_Sesion'] = sessionids
    return result


def events_per_resource(self) -> pd.DataFrame:
    # Calcula el número de accesos por contexto(recurso), sección.
    result = 0
    # result = self.dataframe.groupby([CONTEXTO, ID_RECURSO, SECCION]).size() + result
    # result = result.reset_index()
    # result.rename(columns={0: NUM_EVENTOS})
    # result.columns = ['Recurso', ID_RECURSO, SECCION, NUM_EVENTOS]
    # result = result.sort_values(ascending=False, by=[ID_RECURSO])
    return result


def participants_per_resource(self) -> pd.DataFrame:
    # Calcula el número de participantes por recurso del dataframe.
    # result = self.dataframe.groupby([CONTEXTO, ID_RECURSO, SECCION])[ID_USUARIO].nunique()
    # result = result.reset_index()
    # result.rename(columns={0: NUM_PARTICIPANTES})
    # result.columns = ['Recurso', ID_RECURSO, SECCION, NUM_PARTICIPANTES]
    # result = result.sort_values(ascending=False, by=[ID_RECURSO])
    result = 0
    return result


def merge_part_df(df):

    user_acc = get_part_access(df)
    tareas = df[df.Event == "Se ha enviado una entrega"][['Name']].value_counts().reset_index().rename(
        columns={'Name': 'Usuario', 0: 'N'})
    foros = df[df.Event.isin(ACTIVE_PART_FORO)][['Name']].value_counts().reset_index().rename(
        columns={'Name': 'Usuario', 0: 'N'})
    cuestionarios = df[df.Event.isin(CUESTIONARIO_PART)][['Name']].value_counts().reset_index().rename(
        columns={'Name': 'Usuario', 0: 'N'})
    glosario = df[df.Event.isin(GLOSARY_PART)][['Name']].value_counts().reset_index().rename(
        columns={'Name': 'Usuario', 0: 'N'})

    user_full = user_acc.merge(tareas, how='left', on='Usuario').rename(
        columns={'N': 'Tareas subidas'})
    user_full = user_full.merge(foros, how='left', on='Usuario').rename(
        columns={'N': 'Participación en foros'})
    user_full = user_full.merge(cuestionarios, how='left', on='Usuario').rename(
        columns={'N': 'Cuestionarios completados'})
    user_full = user_full.merge(glosario, how='left', on='Usuario').rename(
        columns={'N': 'Contribuciones al glosario'})

    user_full['Tareas subidas'] = user_full['Tareas subidas'].fillna(0)
    user_full['Tareas subidas'] = user_full['Tareas subidas'].astype(int)
    user_full['Participación en foros'] = user_full['Participación en foros'].fillna(0)
    user_full['Participación en foros'] = user_full['Participación en foros'].astype(int)
    user_full['Cuestionarios completados'] = user_full['Cuestionarios completados'].fillna(0)
    user_full['Cuestionarios completados'] = user_full['Cuestionarios completados'].astype(int)
    user_full['Contribuciones al glosario'] = user_full['Contribuciones al glosario'].fillna(0)
    user_full['Contribuciones al glosario'] = user_full['Contribuciones al glosario'].astype(int)

    return user_full

def merge_course_df(df):

    courses_acc = get_course_list(df)

    df_users_cursos = df[['Curso','Name']].value_counts().reset_index().rename(
            columns={'index': 'Curso', 'Context':'N'})
    df_users_cursos2 = df_users_cursos['Curso'].value_counts().reset_index().rename(
            columns={'index': 'Curso', 'Curso':'N'})

    foros_cant = df[df['Context'].str.contains(r'^Foro')][['Curso','Context']]. \
                    value_counts().reset_index().rename(columns={'index': 'Context', 0:'N'})
    foros_cant = foros_cant['Curso'].value_counts().reset_index(). \
                    rename(columns={'index': 'Curso', 'Curso':'N'})

    foros_parti = df[(df['Event'] == 'Mensaje creado')|(df['Event'] == 'Algún contenido ha sido publicado.')] 
    foros_participacion = foros_parti[foros_parti['Context']. \
                            str.contains(r'^Foro')][['Curso']].value_counts(). \
                            reset_index().rename(columns={'index': 'Context', 0:'N'})

    tarea = df[(df['Event'] == 'Se ha enviado una entrega')|(df['Event'] == 'Se ha entregado una extensión')]
    tarea2 = tarea['Curso'].value_counts().reset_index().rename(columns={'index':'Curso','Curso':'N'})

    cursos_full = pd.DataFrame
    cursos_full = df_users_cursos2.merge(courses_acc, how='left', on='Curso').rename(
            columns={'N':'Participantes'})
    cursos_full = cursos_full.merge(foros_participacion, how='left', on='Curso').rename(
            columns={'N': 'Participación en foros'})
    cursos_full = cursos_full.merge(tarea2, how='left', on='Curso').rename(
             columns={'N': 'Tareas subidas'})

    cursos_full['Tareas subidas'] = cursos_full['Tareas subidas'].fillna(0)
    cursos_full['Tareas subidas'] = cursos_full['Tareas subidas'].astype(int)

    return cursos_full

def create_df_cluster(user_full):
    used_fields = ['Accesos', 'Tareas subidas', 'Participación en foros', \
                    'Cuestionarios completados','Contribuciones al glosario']
    user_full_km = cluster.kmeans_func(
        user_full[used_fields])
    user_pca = cluster.pca_func(
        user_full_km[used_fields])
    user_pca = pd.DataFrame(user_pca, columns=('pca1', 'pca2'))
    user_pca = user_pca.join(user_full_km)
    user_pca = user_pca.join(user_full['Usuario'])
    return user_pca

# ·········

# CONSULTAS ·········


def get_course_total_access(df):
    # Accesos por día
    df2 = df['date'].value_counts().reset_index().rename(
        columns={'index': 'Date', 'date': 'N'}).sort_values('Date')
    return df2


def get_course_num(df) -> int:
    #cadena = "Curso:"
    num_cursos = df['Curso'].value_counts()
    return len(num_cursos)


def get_course_list(df):
    #cadena = "Curso:"
    df_cursos = df['Curso']. \
                value_counts().reset_index().rename(columns={'index': 'Curso', 'Curso': 'Accesos'})
    return df_cursos

def get_course_top10_access(df):
    #cadena = "Curso:"
    df_cursos = df['Curso']. \
                    value_counts().reset_index(). \
                    rename(columns={'index':'Curso', 'Curso':'N'})
    df_contexto = df[['date', 'Curso']].value_counts().reset_index(). \
                rename(columns={'date': 'Fecha', 'Curso': 'Curso', 0: 'N'}).sort_values(by='Fecha')
    cursos = df_cursos['Curso'].head(10)
    df_contexto = df_contexto[(df_contexto.Curso.isin(cursos))]
    return df_contexto

def get_part_access(df):
    df_usr_t1 = df['Name'].value_counts().reset_index().rename(
        columns={'index': 'Usuario', 'Name': 'Accesos'})
    return df_usr_t1


def get_num_participants(df) -> int:
    return df["ID_Usuario"].nunique()  # - num_teachers(self)


def get_num_active_participation(df) -> int:
    result = len(df[df.Event.isin(ACTIVE_PART)])
    return result


def get_num_resource(df) -> int:
    return df["ID_Recurso"].nunique()


def get_num_session(df) -> int:
    return df["ID_Sesion"].nunique()


def get_num_upload_assignments(df) -> int:
    result = len(df[df.Event == "Se ha enviado una entrega"])
    return result


def get_course_headmap(df):
    df2 = df[["wd", "hour"]].value_counts(
    ).reset_index().rename(columns={0: 'N'})
    return df2


def get_comp_acc(df):
    df_comp = df['Component'].value_counts().reset_index().rename(
        columns={'index': 'Component', 'Component': 'N'})
    return df_comp


def get_user_list(df):
    users = sorted(df.Name.unique())
    return users

def get_part_x_act(df):
    df2 = df[df.Context.str.startswith(("Foro","Tarea","Glosario","Cuestionario", "URL"))]     
    df3 = ( df2[['Context','Name']]
            .value_counts()
            .reset_index() 
            .rename(columns={'index': 'Contexto', 0:'N'}) )
    df4 = ( df3[['Context']]
            .value_counts()
            .reset_index() 
            .rename(columns={'Context': 'Contexto', 0:'N'}).sort_values(by='N') )
    return df4

def get_act_acc(df):
    #df2 = df[df.Component.isin(["Foro", "Tarea", "Glosario","Cuestionario", "URL"])]
    df2 = df[df.Context.str.startswith(
        ("Foro", "Tarea", "Glosario", "Cuestionario", "URL"))]
    df3 = (df2[['Context']]
           .value_counts()
           .reset_index()
           .rename(columns={'index': 'Context', 0: 'N'}).sort_values(by='N'))
    return df3


def get_country_count_IP(df):
    database = IP2Location.IP2Location(
        os.path.join(settings.BASE_DIR, 'IP-COUNTRY.BIN'))
    df_ip = df['IP'].value_counts().reset_index().rename(
        # columns={'index': 'IP', 'Dirección IP':'N'})
        columns={'index': 'IP', 'IP': 'N'})

    def find_country_from_ip(ip):
        rec = database.get_all(ip)
        return rec.country_long

    df_ip['Country'] = df_ip.apply(
        lambda x: find_country_from_ip(x['IP']), axis=1)
    df_ip2 = df_ip['Country'].value_counts().reset_index().rename(
        columns={'index': 'Country', 'Country': 'N'})

    countries_codes_and_coordinates = pd.read_csv(os.path.join(
        settings.BASE_DIR, 'countries_codes_and_coordinates.csv'))
    countries_codes_and_coordinates3 = countries_codes_and_coordinates[[
        'Country', 'Alpha-3 code']]

    df_ip2 = df_ip2.merge(countries_codes_and_coordinates3,
                          how='left', on='Country')
    df_ip2['ISO'] = df_ip2['Alpha-3 code'].str.replace('"', '')
    df_ip2['ISO'] = df_ip2['ISO'].str.replace(' ', '')
    df_ip2 = df_ip2.dropna()

    return df_ip2


def del_user_by_name(df, users_name):
    # df = df.loc[df["Name"] != "-"]
    # df = df.loc[df["Name"] != "Gestor General Cursos a Distancia"]
    for user in users_name:
        df = df[~df["Name"].isin([user])]
    return df
