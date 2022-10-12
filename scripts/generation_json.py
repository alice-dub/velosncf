import csv
import json
import pandas as pd
import numpy as np

element = []
type_fichier = "stops"

data = pd.read_csv('{}/{}.txt'.format("TER", type_fichier))
data["stop_name"] = data["stop_name"].replace("/", "-", regex=True)
stop_names = data['stop_name'].unique().tolist()
data_times = pd.read_csv('{}/stop_times.txt'.format("TER"))
trips = pd.read_csv('{}/trips.txt'.format("TER"))
trips = trips[["route_id", "trip_id"]]
routes = pd.read_csv('{}/routes.txt'.format("TER"))
routes = routes[["route_id", "route_type"]]
data_times = pd.merge(data_times, trips, how="left", on=["trip_id"])
data_times = pd.merge(data_times, routes, how="left", on=["route_id"])
data_times = data_times[data_times["route_type"]==2]
liste_noms = []

for stop_name in stop_names:
    print(stop_name)
    data_stop = data[data["stop_name"] == stop_name]
    coordonnees = [data_stop[data_stop["stop_name"] == stop_name]["stop_lon"].iloc[0], data_stop[data_stop["stop_name"] == stop_name]["stop_lat"].iloc[0]]
    stop_ids = data_stop['stop_id'].unique().tolist()
    get_trips_number = data_times[data_times["stop_id"].isin(stop_ids)]
    if len(get_trips_number) > 0:
        liste_noms.append(stop_name)
        trips_ids = get_trips_number['trip_id'].unique().tolist()
        get_trips_number = get_trips_number[["stop_sequence", "trip_id"]]
        get_trips_number = get_trips_number.rename(columns={"stop_sequence": "sequence_reference"})
        data_times_stops = data_times[data_times['trip_id'].isin(trips_ids)]
        data_times_stops = pd.merge(data_times_stops, get_trips_number, how="left", on=["trip_id"])
        data_times_stops = data_times_stops[~data_times_stops["stop_id"].isin(stop_ids)]
        data_times_stops["categorie"] = np.where(data_times_stops["stop_sequence"]>data_times_stops["sequence_reference"],"Arrivée", "Départ")
        
        data_gares = data[["stop_name", "stop_id", "stop_lon", "stop_lat"]]
        data_times_stops = pd.merge(data_times_stops, data_gares, how="left", on=["stop_id"])
        autres_arrets = data_times_stops['stop_name'].unique().tolist()
        geojson = {}
        geojson["type"] = "FeatureCollection"
        geojson["features"] = []
        gares = []
        #Creation du pin point pour la gare choisie
        carac_route = {}
        carac_route["type"] = "Feature"
        carac_route["properties"] = {}
        carac_route["properties"]["start"] = stop_name
        carac_route["properties"]["stop_name"] = stop_name
        carac_route["properties"]["type"] = "Gare sélectionnée"
        carac_route["properties"]["iconstarte"] = "Icon2"
        carac_route["geometry"] = {}
        carac_route["geometry"]["type"] = "Point"
        carac_route["geometry"]["coordinates"] = coordonnees
        geojson["features"].append(carac_route)
        #Creation du pin point pour les autres gares (pour l instant pas d implementation départ/arrivée)
        for gare in autres_arrets:
            carac_route = {}
            carac_route["type"] = "Feature"
            carac_route["properties"] = {}
            carac_route["properties"]["start"] = stop_name
            carac_route["properties"]["stop_name"] = gare
            carac_route["properties"]["type"] = "Gare accessible"
            carac_route["properties"]["icone"] = "TER"
            carac_route["geometry"] = {}
            carac_route["geometry"]["type"] = "Point"
            carac_route["geometry"]["coordinates"] = [data[data["stop_name"] == gare]["stop_lon"].iloc[0],\
                                                        data[data["stop_name"] == gare]["stop_lat"].iloc[0]]
            geojson["features"].append(carac_route)

        with open('gares_accessibles/{}.json'.format(stop_name), 'wt', encoding='utf8') as fp:
            json.dump(geojson, fp)

data_index = data[data["stop_name"].isin(liste_noms)][["stop_name"]].drop_duplicates().sort_values(by="stop_name")
with open('liste_station.json'.format(id), 'wt', encoding='utf8') as fp:
        data_index.to_json(fp, orient="records", force_ascii=False)