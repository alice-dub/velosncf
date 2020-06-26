import csv, sys, json

csv.field_size_limit(sys.maxsize)

lignes_trace = {}


#### Recuperation des gares apparantees a chaque ligne de train 

def formes():
    with open('formes-des-lignes-du-rfn.csv') as forme:
        with open('lignes-par-statut.csv') as nom: 
            with open('liste-des-gares.csv') as gare:
                forme_reader = list(csv.reader(forme, delimiter=';'))
                gare_reader = list(csv.reader(gare, delimiter=';'))
                for row in forme_reader:
                    for row_3 in gare_reader:
                        if row_3[4] == row[2]:
                            if not row[2] in lignes_trace:
                                lignes_trace[row[2]] = set()
                            lignes_trace[row[2]].add(row_3[1])

    print(lignes_trace)

#### Tri des arrets
 
# Lien entres les routes et voyages 

voyages = {}
with open('TER/trips.txt') as trip:
    trip_reader = csv.reader(trip, delimiter=',')
    i = 0
    for row in trip_reader:
        if i > 0:
            if not row[0] in voyages:
                voyages[row[0]] = set()    
            voyages[row[0]].add(row[2])
        i += 1


### Quel est le voyage qui s'arrete sur le plus d'arret ?
nombre_arret = {}
with open('TER/stop_times.txt') as arret:
    arret_reader = csv.reader(arret, delimiter=',')
    i = 0
    for row in arret_reader:
        if i > 0:
            if not row[0] in nombre_arret:
                nombre_arret[row[0]] = 0
            nombre_arret[row[0]] += 1
        i += 1


## Choix du trajet de reference pour chaque route
ref_trajet = {}
for route, trajets in voyages.items():
    arret_max = 0
    trajet_max = ""
    for trajet in trajets:
        nombre_stop = nombre_arret[trajet]
        if nombre_stop > arret_max:
            arret_max = nombre_stop
            trajet_max = trajet
    ref_trajet[trajet_max] = route


## Recuperation des gares de chaque voyage
listes_gares = {}
with open('TER/stop_times.txt') as gares:
    gares_reader = csv.reader(gares, delimiter=',')
    i = 0 
    for row in gares_reader:
        if i > 0:
            if row[0] in ref_trajet:
                if not row[0] in listes_gares:
                    listes_gares[row[0]] = []
                listes_gares[row[0]].append(row[3])
        i += 1

## Recuperation des coordonnees des gares
listes_coordonnes = {}
with open('TER/stops.txt') as coords:
    coords_reader = list(csv.reader(coords, delimiter=','))
    for voyage, gares in listes_gares.items():
        for gare in gares:
            i = 0
            for row in coords_reader:
                if i > 0:
                    if 40 <= float(row[3]) <= 55:
                        if -5 <= float(row[4]) <= 11:
                            if row[0] == gare:
                                if not voyage in listes_coordonnes:
                                    listes_coordonnes[voyage] = []
                                listes_coordonnes[voyage].append([float(row[4]), float(row[3])])
                i += 1

### Creation du geojson 
geojson = {}
geojson["type"] = "FeatureCollection"
geojson["features"] = []
for route, coords in listes_coordonnes.items():
    carac_route = {}
    carac_route["type"] = "Feature"
    carac_route["properties"] = {}
    carac_route["properties"]["id"] = route

    carac_route["geometry"] = {}
    carac_route["geometry"]["type"] = "LineString"
    carac_route["geometry"]["coordinates"] = []
    for coord in coords:
        carac_route["geometry"]["coordinates"].append(coord)
    geojson["features"].append(carac_route)


with open('data2.geojson', 'w') as fp:
    json.dump(geojson, fp)