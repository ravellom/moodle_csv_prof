import os
import tarfile
import pandas as pd
import openpyxl
import xml.etree.ElementTree as ET



def course_structure(df_main, backup) -> pd.DataFrame:
    #Añade la sección a la que pertenece cada recurso dentro del curso de Moodle.
    tarfile.open(fileobj=backup).extract(member='moodle_backup.xml')
    tree = ET.parse('moodle_backup.xml')
    root = tree.getroot()
    df = pd.DataFrame(columns=['Section', 'ID_Recurso', 'Recurso'])
    for activity in root.findall('information/contents/activities/activity'):
        df = df.append(
            pd.Series(
                [activity.find('sectionid').text, activity.find('moduleid').text, activity.find('title').text],
                index=['Section', 'ID_Recurso', 'Recurso']), ignore_index=True)
    id_curso = ''
    for activity in root.findall('information/contents/course'):
        id_curso = activity.find('courseid').text
    dfaux = df_main.copy()
    dfaux['Section'] = id_curso
    for activity, section in zip(df['ID_Recurso'], df['Section']):
        dfaux.loc[dfaux['ID_Recurso'] == float(activity)] = dfaux.loc[
            dfaux['ID_Recurso'] == float(activity)].astype(str).replace(id_curso, section)
    os.remove("moodle_backup.xml")
    return dfaux

def add_section_column(df, backup) -> pd.DataFrame:
    if backup != "":
        df['Section'] = course_structure(df, backup)['Section']
    else:
        df['Section'] = 1