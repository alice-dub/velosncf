import csv
import json

element = []
type_fichier = "stops"

with open('{}/{}.txt'.format("TER", type_fichier), encoding='utf-8') as stop:
    stop_reader = csv.reader(stop, delimiter=',')
    i = 0
    geojson = []
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
                carac_route["stop_name"] = dico["stop_name"]
                carac_route["coordinates"] = [dico["stop_lon"],dico["stop_lat"]]
                geojson.append(carac_route)
        i += 1

    with open('gares.json', 'w') as fp:
        json.dump(geojson, fp)