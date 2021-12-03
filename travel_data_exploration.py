import numpy as np
import pandas as pd

from sodapy import Socrata
from time import time
import osmnx as ox  
import networkx as nx


class GPSCoordinate():

    def __init__(self, lattitude, longitude):
        self.lattitude = lattitude
        self.lat = lattitude
        self.longitude = longitude
        self.lon = longitude

class MapGraph():

    def __init__(self, place, transportation_mode, simplify_map=True):
        t0 = time()
        G = ox.graph_from_place(place, transportation_mode, simplify=simplify_map)
        G = ox.speed.add_edge_speeds(G)
        G = ox.speed.add_edge_travel_times(G)
        self.G = G
        print(f'Map loaded in {time() - t0}')

    def estimate_travel_seconds(self, orig, dest):
        return nx.shortest_path_length(
            G=self.G, 
            source=ox.distance.nearest_nodes(self.G, X=orig.lon, Y=orig.lat),
            target=ox.distance.nearest_nodes(self.G, X=dest.lon, Y=dest.lat),
            weight='travel_time'
            )

    def estimate_travel_minutes(self, orig, dest):
        return self.estimate_travel_seconds(orig, dest) / 60.0


def twelve_hour_time_parts(time, hour_delimiter=':'):
    time_parts = time.split(hour_delimiter)
    hour = int(time_parts[0])
    period = time_parts[-1][-2:].lower()
    return hour, period

def twelve_hour_to_military(time):
    hour, period = twelve_hour_time_parts(time)
    if hour == 12 and period == 'am':
        return 0
    elif hour == 12 and period == 'pm':
        return hour
    elif period == 'pm':
        return hour + 12
    else:
        return hour


def get_traffic_data():
    # This dataset unfortunately proved to have more holes than observations
    # We recommend seeking a different source
    traffic = pd.read_csv('https://data.cityofnewyork.us/api/views/ertz-hr4r/rows.csv?accessType=DOWNLOAD')

    print(traffic.head())
    traffic.info()
    # Convert to pandas DataFrame
    volume_cols = [
       '12:00-1:00 AM', '1:00-2:00AM', '2:00-3:00AM', '3:00-4:00AM',
       '4:00-5:00AM', '5:00-6:00AM', '6:00-7:00AM', '7:00-8:00AM',
       '8:00-9:00AM', '9:00-10:00AM', '10:00-11:00AM', '11:00-12:00PM',
       '12:00-1:00PM', '1:00-2:00PM', '2:00-3:00PM', '3:00-4:00PM',
       '4:00-5:00PM', '5:00-6:00PM', '6:00-7:00PM', '7:00-8:00PM',
       '8:00-9:00PM', '9:00-10:00PM', '10:00-11:00PM', '11:00-12:00AM'
       ]
    traffic[volume_cols] = traffic[volume_cols].fillna(0).astype(int)
    traffic = traffic.groupby('Date').sum()[volume_cols]
    traffic.head()
    traffic = traffic.melt(
        value_vars=volume_cols, 
        var_name='hour_of_day', 
        value_name='vehicle_count', 
        ignore_index=False
        )
    traffic.head()
    traffic['hour_of_day'] = traffic['hour_of_day'] \
        .apply(lambda time: twelve_hour_to_military(time))
    traffic = traffic.reset_index(drop=False)
    traffic['Date'] = pd.to_datetime(traffic['Date']).dt.date
    traffic = traffic.rename(columns={'Date': 'date'})
    traffic.columns
    print(traffic.head())
    return traffic


def get_weather_data():
    # Data documentation https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/GHCND_documentation.pdf 
    # URL pulls in Central Park weather data
    weather = pd.read_csv('https://www.ncei.noaa.gov/orders/cdo/2809500.csv')
    weather = weather[['DATE', 'PRCP', 'SNOW', 'TMIN', 'TMAX']]
    weather.columns = ['date', 'rain_inches', 'snow_inches', 'temp_min_f', 'temp_max_f']
    return weather


if __name__ == '__main__':
    df = pd.read_csv('~/Downloads/df_train_sample.csv')
    df['date'] = pd.to_datetime(df['date']).dt.date
    df.info()

    # Weather
    print('Appending weather data')
    weather = get_weather_data()
    print('Got weather')
    df = df.merge(weather, on='date', how='left')
    df.info()

    # Travel minutes
    travel_minutes = []
    NYC = MapGraph(place="New York City, NY, USA", transportation_mode="drive")
    for _, row in df[['start_lng', 'start_lat', 'end_lng', 'end_lat']].iterrows():
        origin = GPSCoordinate(row['start_lat'], row['start_lng'])
        destination = GPSCoordinate(row['end_lng'], row['end_lat'])
        travel_minutes.append(NYC.estimate_travel_minutes(origin, destination))
    df['travel_minutes'] = travel_minutes
    print(df['travel_minutes'])


    # Traffic
    traffic = get_traffic_data()
    df = df.merge(traffic, on=['date', 'hour_of_day'], how='left')
    df.info()
