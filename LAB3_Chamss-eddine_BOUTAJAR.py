import time
import streamlit as st
# importing numpy and pandas for to work with sample data.
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly_express as px
import streamlit.components.v1 as components
from functools import wraps
# import time

def config():

    st.set_page_config(
        page_title = 'Dashboard',
        page_icon = '✅',
        layout = 'wide')
config()

def log_time(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(args, **kwargs):
        
        start = time.time()
        result = func(args, **kwargs)
        end = time.time()
        f = open("log_dev.txt",'a',encoding="utf8")
        time_res = end - start
        mes = "\n"+func.__name__+ " time = " + str(time_res) + " s" + " un temps plutçot correct"
        f.write(mes)
        return result

    return wrapper
#@st.cache  # 👈 This function will be cached
#def my_slow_function(arg1, arg2):
    # Do something really slow in here!
   # return the_output
# Si le programme ne fonctionne pas, mettre la ligne 16 à 19 en commentaire, j'ai ajouter cette ligne pour un peu plus d'interaction et mettre le site en dark    
st.title('Dashboard pour les deux dataset')
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
@log_time
def read_(chemin):
    dataset=pd.read_csv(chemin)
    return dataset

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
@log_time  
def read1_(chemin):

    dataset1=pd.read_csv(chemin)
    return dataset1

data = read_('C:/Users/chams/Downloads/Data_Viz/ny-trips-data.csv')
df = read1_('C:/Users/chams/Downloads/Data_Viz/uber-raw-data-apr14.csv')




#st.write(data)
#st.write(df)
def get_weekday(df):
    return df.weekday()

def get_dom(df):
    return df.day

def get_hours(df):
    return df.hour

def count_rows(rows):
    return len(rows)

def choix(arg1,arg2):
    choice = [arg1,arg2]
    return choice
choice = choix('Statistiques Uber Avril 2014','New York Trips')    
df_map = pd.DataFrame()
data_map_dropoff = pd.DataFrame()
data_map_pickup = pd.DataFrame()

databar = pd.DataFrame(data[:], columns = ["Date/Time","Lat","Lon"])






#@st.cache(suppress_st_warning=True)
@log_time
def option(arg):
    data = read_('C:/Users/chams/Downloads/Data_Viz/ny-trips-data.csv')
    df = read1_('C:/Users/chams/Downloads/Data_Viz/uber-raw-data-apr14.csv')

    option = st.sidebar.selectbox(arg,choice)

    st.set_option('deprecation.showPyplotGlobalUse', False)
    if option == choice[0]:

        st.title('Statistiques Uber Avril 2014')
        
        st.text("Les 5 premières lignes de la 1er dataset")
        st.write(df.head())
        header_1_column, header_2_column, header_3_column = st.columns(3)

        date_debut = header_1_column.date_input(
            "Date de debut",
            datetime.date(2014, 4, 1))

        date_fin = header_2_column.date_input(
            "Date de fin",
            datetime.date(2014, 4, 30))

        pressed = header_3_column.button('Rechercher')
        clique = header_3_column.button('Rechercher les courses')
        if pressed:
            mask = (df['Date/Time'].dt.date > date_debut) & (df['Date/Time'].dt.date <= date_fin)
            df = df.loc[mask]
            
        if clique:
            mask = (data['Date/Time'].dt.date > date_debut) & (data['Date/Time'].dt.date <= date_fin)
            df = df.loc[mask]
            df.rename(columns={'Lat': 'lat', 'Lon': 'lon'}, inplace=True)
            st.write(df)
            st.map(df)

        df['Date/Time']=pd.to_datetime(df['Date/Time'])
        df['hours']= df['Date/Time'].map(get_hours)
        df['dom']= df['Date/Time'].map(get_dom)
        df['weekday']= df['Date/Time'].map(get_weekday)
        
        df_map['lon'] = df['Lon']
        df_map['lat'] = df['Lat']
        st.title('Localisation des courses')
        st.map(df_map)
        by_dayt= df.groupby('weekday').mean()
        st.title('Lieux et dates de prise en charge des courses')
        st.write(by_dayt)
        st.title('Graphique représentant le nombre de courses en moyenne par jour')
        graph=px.bar(by_dayt,y="dom")
        st.plotly_chart(graph)
        
        #.hist(bins = 30, rwidth=0.8, range=(0.5, 30.5))
        #plt.show()
        #st.pyplot()
        
        #st.line_chart(df_map['weekday'])
        
        frqDay1_column = st.columns(2)
        st.title('Fréquence de course par jour en un mois')
        df[["dom"]].plot.hist(bins = 30, rwidth=0.8, range=(0.5,30.5), figsize = (30,15) , title = "Pick - Fréquence des course par jour - Uber - April 2014")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        st.title("Fréquence de course par jour en fonction de l'heure")
        dataByDayAndHours = df.groupby(['weekday','hours']).apply(count_rows).unstack()
        fig4, ax = plt.subplots()
        sns.heatmap(dataByDayAndHours, linewidths = .5)
        st.pyplot(fig4)

        
    elif option == choice[1]:
        st.title('New York Trips')
    
        st.text("Les 5 premières lignes de la 2eme dataset")
        st.write(data.head())

        header_1_column, header_2_column, header_3_column = st.columns(3)

        date_debut = header_1_column.date_input(
            "Date de debut",
            datetime.date(2014, 4, 1))

        date_fin = header_2_column.date_input(
            "Date de fin",
            datetime.date(2014, 4, 30))

        pressed = header_3_column.button('Rechercher')
        clique = header_3_column.button('Rechercher les courses')
        if pressed:
            mask = (data['Date/Time'].dt.date > date_debut) & (data['Date/Time'].dt.date <= date_fin)
            data = df.loc[mask]
            
        if clique:
            mask = (data['Date/Time'].dt.date > date_debut) & (data['Date/Time'].dt.date <= date_fin)
            data = data.loc[mask]
            data.rename(columns={'Lat': 'lat', 'Lon': 'lon'}, inplace=True)
            st.write(data)
            st.map(data)
        
        
        data['tpep_pickup_datetime']=pd.to_datetime(data['tpep_pickup_datetime'])
        data['tpep_dropoff_datetime']=pd.to_datetime(data['tpep_dropoff_datetime'])
        data['hours-pickup']= data['tpep_pickup_datetime'].map(get_hours)
        data['hours-drop']= data['tpep_dropoff_datetime'].map(get_hours)
        data['dom-pickup']= data['tpep_pickup_datetime'].map(get_dom)
        data['dom-drop']= data['tpep_dropoff_datetime'].map(get_dom)
        data['weekday-pickup']= data['tpep_pickup_datetime'].map(get_weekday)
        data['weekday-drop']= data['tpep_dropoff_datetime'].map(get_weekday)
        
        data_map_dropoff['lon'] = data['dropoff_longitude']
        data_map_dropoff['lat'] = data['dropoff_latitude']
        st.title('Localisation des courses')
        st.map(data_map_dropoff)
        
        data_map_pickup['lon'] = data['pickup_longitude']
        data_map_pickup['lat'] = data['pickup_latitude']
        st.map(data_map_pickup)

        #data.hist(bins = 30, rwidth=0.8, range=(0.5, 30.5))
        #plt.show()
        #st.pyplot()
        by_passenger_count= data.groupby('passenger_count').mean()
        st.write(by_passenger_count)
        st.title('Graphique représentant le nombre de passagers en fonction de la distance du trajet')
        graph=px.bar(by_passenger_count,y="trip_distance")
        st.plotly_chart(graph)
        

        frqDay_1_column, frqDay_2_column = st.columns(2)
        frqDay_1_column.text('Prise en charge des clients')
        data[["dom-pickup"]].plot.hist(bins = 30, rwidth=0.8, range=(0.5,30.5), figsize = (30,15) , title = "Pick - Fréquence des course par jour - Uber - April 2014")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        
        frqDay_1_column.pyplot()
        st.title("Fréquence de prise d'un client par jour")
        frqDay_2_column.text('Dépôt des clients')
        data[["dom-drop"]].plot.hist(bins = 30, rwidth=0.8, range=(0.5,30.5), figsize = (30,15) , title = "Drop - Fréquence des course par jour - Uber - April 2014")
        st.set_option('deprecation.showPyplotGlobalUse', False)
    
        frqDay_2_column.pyplot()
    
        dataByDayAndHoursDrop = data.groupby(['weekday-pickup','hours-pickup']).apply(count_rows).unstack()
        fig4, ax = plt.subplots()
        sns.heatmap(dataByDayAndHoursDrop, linewidths = .5)
        st.pyplot(fig4)
        
        dataByDayAndHoursDrop = data.groupby(['weekday-drop','hours-drop']).apply(count_rows).unstack()
        fig4, ax = plt.subplots()
        sns.heatmap(dataByDayAndHoursDrop, linewidths = .5)
        st.pyplot(fig4)
        st.title("Fréquence de dépôt du client par jour en fonction de l'heure")
option('Choisissez la dataset')    
components.html("""
<link href="https://unpkg.com/tailwindcss@%5E2/dist/tailwind.min.css" rel="stylesheet">
<div class="max-w-sm rounded overflow-hidden shadow-lg mx-auto my-8">
    <img class="w-full" src="https://media-exp1.licdn.com/dms/image/C5603AQEUyE3mDlpuFQ/profile-displayphoto-shrink_200_200/0/1619365937377?e=1632960000&v=beta&t=XpKtH_PFxR-Fro-VHxjSJnHBT6PFZ5x3WUrevpLipYA" alt="Sunset in the mountains">
    <div class="px-6 py-4">
      <div class="font-bold text-xl mb-2">Futur Data Scientist</div>
      <p class="text-gray-600 text-base">
        Voici donc mon travail sur deux datasets, l'une sur les données uber de septembre 2014 et l'autre concernant les courses à New York !
      </p>
    </div>
    <div class="px-6 py-4">
      <span class="inline-block bg-gray-100 rounded-full px-3 py-1 text-sm font-semibold text-gray-600 mr-2">#DataViZ</span>
      <span class="inline-block bg-gray-100 rounded-full px-3 py-1 text-sm font-semibold text-gray-600 mr-2">#Dataset</span>
      
    </div>
  </div>
      </div>
    """,
    height=600,

)


