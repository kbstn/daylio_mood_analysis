#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 15 17:34:13 2022
ASAS
@author: 
"""

import streamlit as st
import pandas as pd
from scipy.stats import zscore
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
    
import processing
import plot

st.set_page_config(layout="wide")



st.title('Zscore and more :eyes:')
st.text('v.0.2')


# we also create a sidebar
st.sidebar.header("Choose settings")


option = st.sidebar.selectbox(
     'Who are You?',
     ('Koni','Flo'  ))

if option == 'Koni':
    mood_dict={"Lausig":1, "Schlecht":2, "Ok":3,"Gut":4, "Super":5}

else:
    mood_dict={"awful":1, "bad":2, "meh":3,"mixed/unsure":4, "not bad":5, "good":6, "full relax":7,"rad":8}

# create a slider at the sidebar to change the window for rolling mean

window = st.sidebar.slider("Window for rolling mean of mood", 5, 200, 50)

window_weight = st.sidebar.slider("Window for rolling mean of weight", 5, 200, 50)

st.header('Upload a Daylio export .csv file')

# this parts enable filepoload
uploaded_file = st.file_uploader(
        "",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

if uploaded_file is not None:
    file_container = st.expander("Check your uploaded .csv")
    shows_mood = pd.read_csv(uploaded_file)
    uploaded_file.seek(0)
    file_container.write(shows_mood)

else:

     st.info(
         f"""
             👆 Upload a .csv file first. 
             """
     )

     st.stop()
    

# funktion that reads shows_mood.copy and returns a pd dataframe 
# with a datetime index and zscore claculated on a given columns
# and a zscore_smooth based on a rolling mean driven by a 'window' variable


### prepare the data
mood_data = processing.process_data(shows_mood,mood_dict,window)
st.write(mood_data['mood_num'].dtype)


# create the lineplot
# mood_lineplot = plot.create_lineplot(mood_data,y_col="zscore_smooth",title='avg Zscore of my MOOD',target_line=0,target_line_width=4)
mood_lineplot = plot.plot_double_axis(mood_data,'mood_num','zscore_smooth')
st.header('Mood')
st.plotly_chart(mood_lineplot, use_container_width=True)    

st.header('Upload a openscale export .csv file to check your weight data')

# create the same workflow for openscale data
# this parts enable filepoload
uploaded_file2 = st.file_uploader(
        "",
        key="2",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

if uploaded_file2 is not None:
    file_container2 = st.expander("Check your uploaded .csv")
    shows_weight = pd.read_csv(uploaded_file2)
    uploaded_file2.seek(0)
    file_container2.write(shows_weight)

else:

     st.info(
         f"""
             👆 Upload a .csv file first. 
             """
     )

     st.stop()
    

# funktion that reads shows_mood.copy and returns a pd dataframe 
# with a datetime index and zscore claculated on a given columns
# and a zscore_smooth based on a rolling mean driven by a 'window' variable


### prepare the data
weight_data = shows_weight.copy()
#drop nan where no weight
weight_data=weight_data.dropna(subset=['weight'])

weight_data = processing.set_datetimeindex(weight_data,date_col="dateTime")

# calculate zscore
weight_data = processing.calculate_zscore(weight_data,column='weight')

# calculate rolling average
weight_data = processing.calculate_rolling_average(weight_data, window_weight)
# create the lineplot

# weight_lineplot = plot.create_lineplot(weight_data,y_col="zscore_smooth",
# title='avg Zscore of my weight',target_line=0,target_line_width=4,
# target_plot_color='#40B0A6')
weight_lineplot = plot.plot_double_axis(weight_data,'weight','zscore_smooth')
st.header('Weight')
st.plotly_chart(weight_lineplot, use_container_width=True)    

st.header('Mood and Weight')
combined_lineplot = plot.plot_two_df(mood_data,weight_data,y_col='zscore_smooth',title='both plots combined',grid=True)

st.plotly_chart(combined_lineplot, use_container_width=True)    


