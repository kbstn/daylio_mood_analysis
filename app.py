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

import processing
import plot

st.set_page_config(layout="wide")



st.title('Zscore and more 8-)')
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


# create the lineplot
mood_lineplot = plot.create_lineplot(mood_data,y_col="zscore_smooth",title='avg Zscore of my MOOD',target_line=0,target_line_width=4)

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

# calculate zscore
weight_data = processing.calculate_zscore(weight_data,column='weight')

# calculate rolling average
weight_data = processing.calculate_rolling_average(weight_data, window_weight)

# create the lineplot
weight_lineplot = plot.create_lineplot(weight_data,y_col="zscore_smooth",
title='avg Zscore of my weight',target_line=0,target_line_width=4,
target_plot_color='#40B0A6')

st.header('Weight')
st.plotly_chart(weight_lineplot, use_container_width=True)    

st.header('Mood and Weight')
combined_lineplot = plot.plot_two_df(mood_data,weight_data,y_col='zscore_smooth',title='both plots combined',grid=True)

st.plotly_chart(combined_lineplot, use_container_width=True)    



# # create a histogram for the data
# fig_hist = px.histogram(mood_data['mood_num'],title="<b>Histogram of my 'my mood' choices</b>",#er Gender",  "day": "Day of Week", "total_bill": "Receipts"},
#             # category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "sex": ["Male", "Female"]},
#             # color_discrete_map={"Male": "RebeccaPurple", "Female": "MediumPurple"},
#             template="simple_white"
#             )

# fig_hist.update_layout({
# 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
# 'paper_bgcolor': 'rgba(0, 0, 0, 0)'
# })


# st.plotly_chart(fig_hist, use_container_width=True)    



# ### barplot for count of votes, grouped by weekday
# bar_votes = mood_data[['mood','weekday']].groupby('weekday').count().rename(columns={'mood':'Vote_Numbers'})

# ## barplot for count of moods grouped by weekday





# # bar_days = mood_data[['mood','weekday']].groupby(['weekday','mood']).count()
# bar_days = mood_data[mood_data.zscore >0][['mood','weekday']].groupby('weekday').count()
# ## barplot for count of moods grouped by weekday

# fig_bar = px.bar(
#     bar_days,
#     x=bar_days.index,
#     y="mood",
#     title="<b>Number of days with zscore > 0</b>",
#     color_discrete_sequence=["#0083B8"] * len(bar_days),
#     template="plotly_white",
# )
# fig_bar.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )
# st.plotly_chart(fig_bar, use_container_width=True)    



# st.write(mood_data)

