import csv
import json

element = []
type_fichier = "stops"

with open('{}/{}.txt'.format("TER", type_fichier), encoding='utf-8') as stop:
    stop_reader = csv.reader(stop, delimiter=',')
    i = 0
    geojson = {}
    geojson["type"] = "FeatureCollection"
    geojson["features"] = []
    gares = []
    for row in stop_reader:
        if i == 0:
            keys = row
        else:
            dico = {}
            for i in range(len(row)):
                dico[keys[i]] = row[i].replace("'\'", " ")
            if dico["stop_name"] not in gares:
                gares.append(dico["stop_name"])
                carac_route = {}
                carac_route["type"] = "Feature"
                carac_route["properties"] = {}
                carac_route["properties"]["stop_name"] = dico["stop_name"]
                carac_route["geometry"] = {}
                carac_route["geometry"]["type"] = "Point"
                carac_route["geometry"]["coordinates"] = [dico["stop_lon"],dico["stop_lat"]]
                geojson["features"].append(carac_route)
        i += 1

    with open('station_point.json', 'w') as fp:
        json.dump(geojson, fp)

