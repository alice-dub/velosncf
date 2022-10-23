import json
import pandas as pd
import numpy as np
import sys

element = []
type_fichier = "stops"
liste_moyens = ["TER", "TGV", "intercite", "transilien", "carTER"]
#liste_moyens = ["TGV"]


###TO DO : Ajouter les exceptions pour gérer les erreurs d'API !!

mise_en_forme = {"TER" : "🚲 ❤️ Train TER 🚆",\
                "TGV" : "🚲 💔 TGV 🚄",\
                "intercite":"🚲 ❤️ Intercité 🚆",\
                "transilien":"🚲 ❤️ Transilien 🚆",\
                "carTER": "🚲 💔 Car TER 🚍"}
data_index = None
liste_nombre = []
periode_analyse = {"TER" : {"debut":"", "fin":""},\
                "TGV" : {"debut":"", "fin":""},\
                "intercite":{"debut":"", "fin":""},\
                "transilien":{"debut":"", "fin":""},\
                "carTER": {"debut":"", "fin":""}}

for moyen in liste_moyens:
    if moyen == "carTER":
        moyen2 = "TER"
    else:
        moyen2 = moyen
    data = pd.read_csv('historiques/{}/{}/{}.txt'.format(sys.argv[1],moyen2, type_fichier))
    data["stop_name"] = data["stop_name"].replace("/", "-", regex=True)
    stop_names = data['stop_name'].unique().tolist()
    data_times = pd.read_csv('historiques/{}/{}/stop_times.txt'.format(sys.argv[1],moyen2))

    trips = pd.read_csv('historiques/{}/{}/trips.txt'.format(sys.argv[1], moyen2))
    trips = trips[["route_id", "trip_id", "service_id"]]
    routes = pd.read_csv('historiques/{}/{}/routes.txt'.format(sys.argv[1],moyen2))
    routes = routes[["route_id", "route_type"]]
    services = pd.read_csv('historiques/{}/{}/calendar_dates.txt'.format(sys.argv[1], moyen2))
    services = services[["service_id","date"]]
    debut = str(services["date"].min())
    fin = str(services["date"].max())
    periode_analyse[moyen]["debut"] = "{}/{}/{}".format(debut[6:8],debut[4:6],debut[:4])
    periode_analyse[moyen]["fin"] = "{}/{}/{}".format(fin[6:8],fin[4:6],fin[:4])
    nombre_jours_total = len(services["date"].unique()) #Hypothese : des trains circulent tous les jours
    data_times = pd.merge(data_times, trips, how="left", on=["trip_id"])
    data_times = pd.merge(data_times, routes, how="left", on=["route_id"])
    if moyen == "carTER":
        data_times = data_times[data_times["route_type"]==3]
    elif moyen == "TER":
        data_times = data_times[data_times["route_type"]==2]
    liste_noms = []

    for stop_name in stop_names:
        data_stop = data[data["stop_name"] == stop_name]
        coordonnees = data_stop["stop_lon"].iloc[0], data_stop["stop_lat"].iloc[0]]
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

            #Nombre de trains partants du stop
            services_ids = data_times_stops['service_id'].unique().tolist()
            services_selected = services[services["service_id"].isin(services_ids)]
            nombre_trajets = len(services_selected)
            nombre_trajets_moyen = round(nombre_trajets / nombre_jours_total,2)
            if nombre_trajets_moyen > 0.1: #Si inférieur on considère qu'il sagit d'une erreur de données
                #Creation du pin point pour la gare choisie
                carac_route = {}
                carac_route["type"] = "Feature"
                carac_route["properties"] = {}
                carac_route["properties"]["start"] = stop_name
                carac_route["properties"]["stop_name"] = stop_name
                carac_route["properties"]["type"] = "Gare sélectionnée"
                carac_route["properties"]["transport"] = moyen
                carac_route["properties"]["nombre_trajet_moyen"] = nombre_trajets_moyen
                carac_route["properties"]["transport_legende"] = mise_en_forme[moyen]
                carac_route["geometry"] = {}
                carac_route["geometry"]["type"] = "Point"
                carac_route["geometry"]["coordinates"] = coordonnees
                geojson["features"].append(carac_route)
                #Creation du pin point pour les autres gares (pour l instant pas d implementation départ/arrivée)
                for gare in autres_arrets:
                    #Calcul du nombre de trains qui font ce trajet
                    data_deux_stops = data_times_stops[(data_times_stops['stop_name'] == gare)]
                    services_ids = data_deux_stops['service_id'].unique().tolist()
                    services_selected = services[services["service_id"].isin(services_ids)]
                    nombre_trajets = len(services_selected)
                    nombre_trajets_moyen = round(nombre_trajets / nombre_jours_total,2)
                    if nombre_trajets_moyen > 0.1: #Si inférieur on considere qu li s'agit d'une erreur de données -> trop peu de trajet
                        liste_nombre.append(nombre_trajets_moyen)
                        carac_route = {}
                        carac_route["type"] = "Feature"
                        carac_route["properties"] = {}
                        carac_route["properties"]["start"] = stop_name
                        carac_route["properties"]["stop_name"] = gare
                        carac_route["properties"]["type"] = "Gare accessible"
                        carac_route["properties"]["transport"] = moyen
                        carac_route["properties"]["nombre_trajet_moyen"] = nombre_trajets_moyen
                        carac_route["properties"]["transport_legende"] = mise_en_forme[moyen]
                        carac_route["geometry"] = {}
                        carac_route["geometry"]["type"] = "Point"
                        carac_route["geometry"]["coordinates"] = [data[data["stop_name"] == gare]["stop_lon"].iloc[0],\
                                                                    data[data["stop_name"] == gare]["stop_lat"].iloc[0]]
                    geojson["features"].append(carac_route)

                with open('gares_accessibles_{}/{}.json'.format(moyen, stop_name), 'w', encoding='utf8') as fp:
                    json.dump(geojson, fp)

    if data_index is None:
        data_index = data[data["stop_name"].isin(liste_noms)][["stop_name", "stop_lon", "stop_lat"]].drop_duplicates().sort_values(by="stop_name")
        data_index["transport"] = moyen
    else:
        data_index2 = data[data["stop_name"].isin(liste_noms)][["stop_name", "stop_lon", "stop_lat"]].drop_duplicates().sort_values(by="stop_name")
        data_index2["transport"] = moyen
        data_index = pd.concat([data_index,data_index2]).drop_duplicates().reset_index(drop=True)

data_index_final = data_index[["stop_name", "transport"]].drop_duplicates().groupby('stop_name')['transport'].apply(list).reset_index(name='transport')
data_index_final2 = data_index.groupby('stop_name').agg(stop_lon=('stop_lon', 'mean'), stop_lat=('stop_lat', 'mean')).reset_index()
data_index_final3 = pd.merge(data_index_final2, data_index_final, on="stop_name", how="inner")

liste_nombre_arr = np.asarray(liste_nombre)
print(np.percentile(liste_nombre_arr, np.arange(0, 100, 20)))

with open('liste_station.json', 'w', encoding='utf8') as fp:
    data_index_final3.to_json(fp, orient="records", force_ascii=False)

with open('periode_analyse.json', 'w', encoding='utf8') as fp:
    json.dump(periode_analyse,fp)
