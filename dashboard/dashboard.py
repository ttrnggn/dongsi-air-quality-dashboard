import pandas as pd
import streamlit as st
from helper import *

st.markdown(
    """
    <style>
    .main {
        background-color: #121212;
    }
    """,
    unsafe_allow_html=True
)

normalized_df = pd.read_csv("air_quality.csv")

normalized_df["datetime"] = pd.to_datetime(normalized_df["datetime"])

min_date = normalized_df["datetime"].min()
max_date = normalized_df["datetime"].max()

with st.sidebar:
  st.markdown("Made with streamlit for educational only")
  st.markdown("Username: henryyy")
  st.caption('Copyrigth © Henry Trenggana 2023. All Rights Reserved')


st.header('Dongsi\'s Air Quality Control Center')
st.subheader('Most pollutant')

col1,col2 = st.columns(2)

with col1:
  date = st.date_input(
    label="Select date", min_value=min_date, max_value=max_date, value=min_date
  )

filtered_df = normalized_df[normalized_df['datetime'] == str(date)]

daily_pollutant = get_mostly_pollutan(filtered_df)
aqi_pollutant = get_aqi_pollutant(filtered_df)

st.bar_chart(daily_pollutant, x='pollutant', y='value', color='color')

# Terdapat bug pada tampilan streamlit tentang warna.
# Jika dilihat (hover) pada bar chart, color yang tertulis pada tooltip
# dan color yang tampil terbalik (terjadi pada kondisi yang acak)

max_pollutant = daily_pollutant.loc[daily_pollutant['value'].idxmax()]['pollutant']

st.markdown(
  f'''
  The most pollutant in Dongsi City at <span style="font-weight: bold;">{date}</span> is <span style= "font-weight: bold;font-size:32px"> {max_pollutant}</span>
  ''',
  unsafe_allow_html=True
)

st.markdown("""*there is a bug in streamlit that display the wrong color. The color that supossed to be displayed got inverted. (you can check by hover the bar in the chart)
            """)

st.subheader("Air Quality Index (AQI)")

col1, col2 = st.columns(2)

with col1:
  st.metric("AQI in Dongsi City", value=round(aqi_pollutant["mean"]))

  st.markdown(
    """
    <style>
      .rounded{
        width: 25px;
        height: 25px;
        border-radius:50%;
        display: block;
        margin-bottom: 0.5rem;
      }
      .green{
        background-color:#008000;
      }
      .green::after{
        content:"Good (0-50 AQI)";
        display:block;
        position: relative;
        left: 2rem;
        bottom: 0.15rem;
        width: 320px;
      }
      .yellow{
       background-color:#FFEA00;
      }
      .yellow::after{
        content:"Moderate (51-100 AQI)";
        display:block;
        position: relative;
        left: 2rem;
        bottom: 0.15rem;
        width: 320px;
      }
      .orange{
       background-color:#FF9900;
      }
      .orange::after{
        content:"Unhealthy for Sensitive Group (101-150 AQI)";
        display:block;
        position: relative;
        left: 2rem;
        bottom: 0.15rem;
        width: 320px;
      }
      .red{
       background-color:#FF0000;
      }
      .red::after{
        content:"Unhealthy (151-200 AQI)";
        display:block;
        position: relative;
        left: 2rem;
        bottom: 0.15rem;
        width: 320px;
      }
      .purple{
       background-color:#C000FF;
      }
      .purple::after{
        content:"Very Unhealthy (201-300 AQI)";
        display:block;
        position: relative;
        left: 2rem;
        bottom: 0.15rem;
        width: 320px;
      }
      .maroon{
       background-color:#800000;
      }
      .maroon::after{
        content:"Hazardous (301+ AQI)";
        display:block;
        position: relative;
        left: 2rem;
        bottom: 0.15rem;
        width: 320px;
      }
    </style>
    <span class="rounded green"></span>
    <span class="rounded yellow"></span>
    <span class="rounded orange"></span>
    <span class="rounded red"></span>
    <span class="rounded purple"></span>
    <span class="rounded maroon"></span>
    """,
    unsafe_allow_html=True
  )
with col2:
  st.map(aqi_pollutant, color = aqi_pollutant['mean'].apply(get_color)[0])


st.subheader("Time to time air quality")

col1, col2 = st.columns(2)

with col1:
  start_date = st.date_input(label="Select start date", min_value=min_date, max_value=max_date, value=min_date)
with col2:
  end_date = st.date_input(label="Select end date", min_value=start_date, max_value=max_date, value=max_date)

time_df = normalized_df[(normalized_df["datetime"] >= str(start_date)) &
                 (normalized_df["datetime"] <= str(end_date))]

time_aqi_df = get_aqi_pollutant(time_df)

time_aqi_df.rename(columns={
  "mean": "AQI",
  "datetime": "Date"
}, inplace=True)

st.line_chart(time_aqi_df, x=str('Date'), y='AQI')