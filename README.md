# Mood Dashboard

In this dashboard you can upload data from the mood tracking app daylio. This app tracks within categories,
to get a somewhat meaningful analysis of very subjective mood data we use the following approach:\n
- map numbers to the moods
- calculate a zscore that measures how many standard deviations the daily mood choice is from the mean
- apply a rolling mean to give you more room for interpretations (you can change it at the side bar)\n

In the second part you can upload weight data from openscale and get a similar result (no example yet)


## Setup streamlit

```
pip install streamlit
```
## navigate to dice.py folder
```
cd /pathtofile/
```

## run app on localhost
```
streamlit run app.py
```
