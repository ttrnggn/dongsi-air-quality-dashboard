import pandas as pd

def get_mostly_pollutan(df):
  melted_df = pd.melt(df, id_vars=['datetime'], var_name='pollutant', value_name='value')
  melted_df['color'] = melted_df['value'].apply(lambda x: '#F05454' if x == melted_df['value'].max() else '#30475E')
  return melted_df

def get_aqi_pollutant(df):
  df = df.set_index('datetime')
  aqi_df = df * 100
  
  mean = aqi_df.mean(axis=1)
  aqi_df["mean"] = mean
  aqi_df["latitude"] = 39.9320
  aqi_df['longitude'] = 116.4341

  aqi_df = aqi_df.reset_index()

  aqi_df['datetime'] = pd.to_datetime(aqi_df['datetime'])

  return aqi_df


def get_color(df):
  if df >= 0 and df <= 50:
    return '#008000'
  elif df >= 51 and df <= 100:
    return '#FFEA00'
  elif df >= 101 and df <=150:
    return '#FF9900'
  elif df >= 151 and df <= 200:
    return '#FF0000'
  elif df >= 201 and df <= 300:
    return '#C000FF'
  else:
    return '#800000'