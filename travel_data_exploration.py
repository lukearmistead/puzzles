import numpy as np
import pandas as pd

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


def get_traffic_data():
    #!/usr/bin/env python

    # make sure to install these packages before running:
    # pip install pandas
    # pip install sodapy

    import pandas as pd
    from sodapy import Socrata

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cityofnewyork.us", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.cityofnewyork.us,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("ertz-hr4r", limit=2000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    print(results_df.head())
    print(results_df.info())



if __name__ == '__main__':

    df = pd.read_csv('~/Downloads/df_train_sample.csv')
    df.info()
    travel_minutes = []
    NYC = MapGraph(place="New York City, NY, USA", transportation_mode="drive")
    for _, row in df[['start_lng', 'start_lat', 'end_lng', 'end_lat']].iterrows():
        origin = GPSCoordinate(row['start_lat'], row['start_lng'])
        destination = GPSCoordinate(row['end_lng'], row['end_lat'])
        travel_minutes.append(NYC.estimate_travel_minutes(origin, destination))
    df['travel_minutes'] = travel_minutes
    print(df['travel_minutes']) 
    
