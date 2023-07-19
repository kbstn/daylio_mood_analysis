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



st.title('Check your mood :eyes:')
st.text('v.0.3c')


# we also create a sidebar
st.sidebar.header("About")

st.sidebar.info("""In this dashboard you can upload data from the mood tracking app daylio. This app tracks within categories,
to get a somewhat meaningful analysis of very subjective mood data we use the following approach:\n
- map numbers to the moods
- calculate a zscore that measures how many standard deviations the daily mood choice is from the mean
- apply a rolling mean to give you more room for interpretations (you can change it at the side bar)\n

In the second part you can upload weight data from openscale and get a similar result (no example yet)""")

st.sidebar.header("Choose settings")


option = st.sidebar.selectbox(
     'Who are You?',
     ('example','Koni','Flo'  ))

if option == 'Koni':
    mood_dict={"Lausig":1, "Schlecht":2, "Ok":3,"Gut":4, "Super":5}

elif option == 'example':
    mood_dict={"Awful":1, "Bad":2, "Normal":3,"Good":4, "Amazing":5}

else:
    mood_dict={"awful":1, "bad":2, "meh":3,"mixed/unsure":4, "not bad":5, "good":6, "full relax":7,"rad":8}

# create a slider at the sidebar to change the window for rolling mean

window = st.sidebar.slider("Window for rolling mean of mood", 5, 200, 50)

window_weight = st.sidebar.slider("Window for rolling mean of weight", 5, 200, 50)





st.header('Upload your own Daylio export .csv file')

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
    #file_container.write(shows_mood)

else:
    shows_mood = pd.read_csv('daylio_example_corrected.csv')

    

# funktion that reads shows_mood.copy and returns a pd dataframe 
# with a datetime index and zscore claculated on a given columns
# and a zscore_smooth based on a rolling mean driven by a 'window' variable


### prepare the data
mood_data = processing.process_data(shows_mood,mood_dict,window)


# set start and end date for the plots
# start_date = st.sidebar.date_input('Start date', pre_mood_data.index.min())
# end_date = st.sidebar.date_input('End date', pre_mood_data.index.max())

# if start_date < end_date:
#     st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
# else:
#     st.error('Error: End date must fall after start date.')

# mood_data =pre_mood_data.loc[start_date:end_date]


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

weight_data = processing.set_datetimeindex(weight_data,date_col="dateTime")

# Step 1: Sort the DataFrame by the datetime index (if not already sorted)
weight_data.sort_index(inplace=True)

# Step 2: Group by date and aggregate the weight data
weight_data_daily = weight_data.groupby(weight_data.index.date)['weight'].mean()

# Step 3: Create a new DataFrame with daily frequency using reindex
idx = pd.date_range(start=weight_data.index.min(), end=weight_data.index.max(), freq='D')
weight_data_daily = weight_data_daily.reindex(idx)

# Step 4: Interpolate linearly to fill in the missing data (NaN values)
weight_data_daily = weight_data_daily.interpolate(method='linear')
# #drop nan where no weight
# weight_data=weight_data.dropna(subset=['weight'])

# weight_data = processing.set_datetimeindex(weight_data,date_col="dateTime")

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

# # change dowenload file size
# config = {
#   'toImageButtonOptions': {
#     'format': 'png', # one of png, svg, jpeg, webp
#     'filename': 'custom_image',
#     'height': 1080,
#     'width': 1920,
#     'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
#   }
# }



# st.plotly_chart(combined_lineplot, use_container_width=False, **{'config': config})
