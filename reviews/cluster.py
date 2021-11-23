from django.shortcuts import render
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from . import my_globals

######  K-means analysis
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.decomposition import PCA

def kmeans_func(df):
        # Creating our Model
        kmeans = KMeans(n_clusters = 2)
        # Training our model
        DF_NORM  = preprocessing.normalize(df) # Normalizing the data
        try:
                kmeans.fit(DF_NORM)
        except:
                return "Se necesitan más de 2 participantes para el análisis de cluster"
        # You can see the labels (clusters) assigned for each data point with the function labels_
        kmeans.labels_
        # Assigning the labels to the initial dataset
        df['cluster'] = kmeans.labels_
        return df

def pca_func(df):
        #Reducing data dimensions 
        PCA_ = PCA(n_components = 2).fit(df)
        # Applying the PCA
        PCA_2 = PCA_.transform(df)
        return PCA_2

