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

st.set_page_config(layout="wide")


st.title('Upload a Daylio export .csv file')



# we also create a sidebar
st.sidebar.header("Choose settings")


option = st.sidebar.selectbox(
     'Who are You?',
     ('Flo', 'Koni'))

if option == 'Koni':
    mood_dict={"Lausig":1, "Schlecht":2, "Ok":3,"Gut":4, "Super":5}

else:
    mood_dict={"awful":1, "bad":2, "meh":3,"mixed/unsure":4, "not bad":5, "good":6, "full relax":7,"rad":8}

# create a slider at the sidebar to change the window for rolling mean

window = st.sidebar.slider("Window for rolling mean", 5, 200, 50)



# this parts enable filepoload
uploaded_file = st.file_uploader(
        "",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

if uploaded_file is not None:
    file_container = st.expander("Check your uploaded .csv")
    shows = pd.read_csv(uploaded_file)
    uploaded_file.seek(0)
    file_container.write(shows)

else:
    st.info(
        f"""
            👆 Upload a .csv file first. Sample to try: [biostats.csv](https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv)
            """
    )

    st.stop()
    




### prepare the data

filter_daylio = shows.copy()
# set the datecolumn as index
filter_daylio.index = pd.to_datetime(filter_daylio["full_date"])
    
filter_daylio["mood_num"] = filter_daylio["mood"].map(mood_dict)
# calculate z score
filter_daylio["zscore"] = zscore(filter_daylio["mood_num"])
# calculate rolle average#
filter_daylio["zscore_smooth"] = filter_daylio["zscore"].rolling(window, min_periods=int(window*0.55)).mean()


# create the lineplot
fig_line=px.line(filter_daylio, x=pd.to_datetime(filter_daylio["full_date"]), y='zscore_smooth',template="simple_white",title="<b>My mood over time</b>")

fig_line.add_shape( # add a horizontal "target" line
    type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=0, y1=0, yref="y"
)
fig_line.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=True)),
)

#    
st.plotly_chart(fig_line, use_container_width=True)    



# create a histogram for the data
fig_hist = px.histogram(filter_daylio['mood_num'],title="<b>Histogram of my 'my mood' choices</b>",#er Gender",  "day": "Day of Week", "total_bill": "Receipts"},
            # category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "sex": ["Male", "Female"]},
            # color_discrete_map={"Male": "RebeccaPurple", "Female": "MediumPurple"},
            template="simple_white"
            )

fig_hist.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)'
})


st.plotly_chart(fig_hist, use_container_width=True)    



### barplot for count of votes, grouped by weekday
bar_votes = filter_daylio[['mood','weekday']].groupby('weekday').count().rename(columns={'mood':'Vote_Numbers'})

## barplot for count of moods grouped by weekday





# bar_days = filter_daylio[['mood','weekday']].groupby(['weekday','mood']).count()
bar_days = filter_daylio[filter_daylio.zscore >0][['mood','weekday']].groupby('weekday').count()
## barplot for count of moods grouped by weekday

fig_bar = px.bar(
    bar_days,
    x=bar_days.index,
    y="mood",
    title="<b>Number of days with zscore > 0</b>",
    color_discrete_sequence=["#0083B8"] * len(bar_days),
    template="plotly_white",
)
fig_bar.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
st.plotly_chart(fig_bar, use_container_width=True)    



st.write(filter_daylio)

