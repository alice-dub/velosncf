#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, sys, json
import trainline
import datetime

csv.field_size_limit(sys.maxsize)

lignes_trace = {}


def formes():
    """Recuperation des gares apparentees a chaque lignes physique de train"""
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

 
def recup_gares(type_train, filtre_velo=False):
    """Recuperation pour chaque ligne de train, d'un trajet typique allant dans le maximum de gares"""
    voyages = {}
    reverse_voyages = {}
    with open('{}/trips.txt'.format(type_train)) as trip:
        trip_reader = csv.reader(trip, delimiter=',')
        i = 0
        for row in trip_reader:
            reverse_voyages[row[2]] = row[0]
            if i > 0:
                if not row[0] in voyages:
                    voyages[row[0]] = set()    
                voyages[row[0]].add(row[2])
            i += 1

    nombre_arret = {}
    arret_debut = {}
    arret_fin = {}

    with open('{}/stop_times.txt'.format(type_train)) as arret:
        arret_reader = csv.reader(arret, delimiter=',')
        i = 0
        for row in arret_reader:
            if i > 0:
                if not row[0] in nombre_arret:
                    nombre_arret[row[0]] = 0 
                    arret_debut[row[0]] = row[3]
                nombre_arret[row[0]] += 1
                if row[0] != trip_en_cours:
                    arret_fin[row[0]] = last_arret
            trip_en_cours = row[0]
            last_arret = row[3]
            i += 1

    ref_trajet = {}
    for route, trajets in voyages.items():
        if True == False: #On cleane le fichier uniquement pour les TERS : pour les intercitée et les tgv on doit garder les differentes branches possibles
            arret_max = 0
            trajet_max = ""
            for trajet in trajets:
                nombre_stop = nombre_arret[trajet]
                if nombre_stop > arret_max:
                    arret_max = nombre_stop
                    trajet_max = trajet
            ref_trajet[trajet_max] = route
        else:
            arret_max = {}
            trajet_max = ""
            for trajet in trajets:
                nombre_stop = nombre_arret[trajet]
                debut =  arret_debut[trajet]
                fin = arret_fin[trajet]
                if arret_max.get((debut, fin)): 
                    if nombre_stop > arret_max.get((debut, fin)):
                        arret_max[(debut, fin)] = nombre_stop
                        trajet_max = trajet
                        ref_trajet[trajet_max] = route
                else:
                    arret_max[(debut, fin)] = nombre_stop
                    trajet_max = trajet
                    ref_trajet[trajet_max] = route                  
    

    listes_gares = {}
    with open('{}/stop_times.txt'.format(type_train)) as gares:
        gares_reader = csv.reader(gares, delimiter=',')
        i = 0 
        for row in gares_reader:
            if i > 0:
                if row[0] in ref_trajet:
                    if not row[0] in listes_gares:
                        listes_gares[row[0]] = []
                    listes_gares[row[0]].append(row[3])
            i += 1
    

    #Recuperation du nom de la route:
    listes_routes = {}
    with open('{}/routes.txt'.format(type_train)) as routes:
        route_reader = csv.reader(routes, delimiter=',')
        i = 0 
        for row in route_reader:
            if i > 0:
                listes_routes[row[0]] = [row[3], row[5]]
            i += 1

    listes_coordonnes = {}
    liste_coordonnes_check = []
    nom = {}
    with open('{}/stops.txt'.format(type_train)) as coords:
        coords_reader = list(csv.reader(coords, delimiter=','))
        for voyage, gares in listes_gares.items():
            if int(listes_routes[reverse_voyages[voyage]][1]) == 2: #On selectionne uniquement les trains (exclusion des bus)
                for gare in gares:
                    i = 0
                    for row in coords_reader:
                        if i > 0:
                            if 40 <= float(row[3]) <= 55:
                                if -5 <= float(row[4]) <= 11:
                                    if row[0][-8:] == gare[-8:]:
                                        if not voyage in listes_coordonnes:
                                            listes_coordonnes[voyage] = []
                                        listes_coordonnes[voyage].append([float(row[4]), float(row[3])])
                                        nom[voyage] = listes_routes[reverse_voyages[voyage]][0]
                        i += 1
    
    for key,item in listes_coordonnes.items():
        liste_coordonnes_check.append(set(map(tuple, item)))

    listes_coordonnes_final = {}
    for key,item in listes_coordonnes.items():
        for item2 in liste_coordonnes_check:
            if set(map(tuple, item)).issubset(item2) and len(item) < len(item2):
                pass
            else:
                listes_coordonnes_final[key] = item
    
    #Mise en commun des traces
    listes_coordonnes_final2 = {}
    nom_legende = {}
    for voyage, coord in listes_coordonnes_final.items():
        for voyage2, legende in nom.items():
            if voyage2 == voyage:
                if listes_coordonnes_final2.get((legende, coord[0][0], coord[-1][0])) is None and listes_coordonnes_final2.get((legende, coord[-1][0], coord[0][0])) is None:
                    listes_coordonnes_final2[(legende, coord[0][0], coord[-1][0])] = []
                    nom_legende[(legende, coord[0][0], coord[-1][0])] = legende
                    for c in coord:
                        listes_coordonnes_final2[(legende, coord[0][0], coord[-1][0])].append(c)
                elif listes_coordonnes_final2.get((legende, coord[-1][0], coord[0][0])):
                    for c in coord:
                        listes_coordonnes_final2[(legende, coord[-1][0], coord[0][0])].append(c)
                else:
                    for c in coord:
                        listes_coordonnes_final2[(legende, coord[0][0], coord[-1][0])].append(c) 

    listes_coordonnes_final21 = {}
    if type_train == "TGV": #On vert éviter d'assenbler par mégarde des lignes TGVs différentes
        limite = 3
    else:
        limite = 2

    #Heuristique répétée deux fois
    for voyage, coord in listes_coordonnes_final2.items():
        doublon = False
        for voyage2, coord2 in listes_coordonnes_final2.items():
            i = 0
            j = 0
            if voyage2 != voyage:
                for c in coord2:
                    if voyage[1] == c[0]:
                        i = 1
                        if c[0] != coord2[0][0] and c[0] != coord2[-1][0]:
                            i = 2
                    if voyage[2] == c[0]:
                        j = 1
                        if c[0] != coord2[-1][0] and c[0] != coord2[0][0]:
                            j = 2
            if i+j > limite:
                doublon = True
                voyage_inter = voyage2
                coord_inter = coord2
        if not doublon:
            listes_coordonnes_final21[voyage] = coord
        else:
            if listes_coordonnes_final21.get(voyage_inter) is None:
                listes_coordonnes_final21[voyage_inter] = coord_inter
            for c in coord:
                if c not in coord_inter:
                    listes_coordonnes_final21[voyage_inter].append(c)
                        
    listes_coordonnes_final22 = {}
    for voyage, coord in listes_coordonnes_final21.items():
        doublon = False
        for voyage2, coord2 in listes_coordonnes_final21.items():
            i = 0
            j = 0
            if voyage2 != voyage:
                for c in coord2:
                    if voyage[1] == c[0]:
                        i = 1
                        if c[0] != coord2[0][0] and c[0] != coord2[-1][0]:
                            i = 2
                    if voyage[2] == c[0]:
                        j = 1
                        if c[0] != coord2[-1][0] and c[0] != coord2[0][0]:
                            j = 2
            if i+j > limite:
                doublon = True
                voyage_inter = voyage2
                coord_inter = coord2
        if not doublon:
            listes_coordonnes_final22[voyage] = coord
        else:
            if listes_coordonnes_final22.get(voyage_inter) is None:
                listes_coordonnes_final22[voyage_inter] = coord_inter
            for c in coord:
                if c not in coord_inter:
                    listes_coordonnes_final22[voyage_inter].append(c)

    #On réorganise les différents arrets par distance 
    listes_coordonnes_final3 = {}
    for voyage, coord in listes_coordonnes_final22.items():
        listes_coordonnes_final3[voyage] = []
        ordered_c = []
        nombre_elem = len(coord)
        elem_init = coord[0]
        for i in range(nombre_elem):
            distance = {}
            mini = 1000
            for c in coord:
                if c not in ordered_c:
                    distance[(c[0] - elem_init[0])**2 + (c[1] - elem_init[1])**2] = c
                    mini = min((c[0] - elem_init[0])**2 + (c[1] - elem_init[1])**2, mini)
            if len(distance) > 0:
                dist_min = min(distance, key=distance.get)
                ordered_c.append(distance[mini])
                elem_init = distance[mini]

        listes_coordonnes_final3[voyage] = ordered_c

    return listes_coordonnes_final3, nom_legende

def creation_geojson(listes_coordonnes, nom):
    geojson = {}
    geojson["type"] = "FeatureCollection"
    geojson["features"] = []
    for route, coords in listes_coordonnes.items():
        carac_route = {}
        carac_route["type"] = "Feature"
        carac_route["properties"] = {}
        carac_route["properties"]["id_trajet"] = route
        carac_route["properties"]["nom"] = nom.get(route)

        carac_route["geometry"] = {}
        carac_route["geometry"]["type"] = "LineString"
        carac_route["geometry"]["coordinates"] = []
        for coord in coords:
            carac_route["geometry"]["coordinates"].append(coord)
        geojson["features"].append(carac_route)


    with open('data_4.geojson', 'w') as fp:
        json.dump(geojson, fp)

def filtre_velo(listes_coordonnes):
    """ Utilisation de l'API trainline pour identifier les trajets faisables avec un vélo. 
    Non implémenté : pb de captcha"""
    dico_nom = {"Paris Est": "Paris"}
    i = 0
    nom_coord = {}
    date_debut = datetime.datetime.now()
    date_fin = date_debut + datetime.timedelta(days=15)
    with open('{}/stops.txt'.format("TGV")) as coords:
        coords_reader = list(csv.reader(coords, delimiter=','))
        for row in coords_reader:
            if i > 0:
                nom_coord[(float(row[4]), float(row[3]))] = row[1]
            i += 1
    
    for route, coords in listes_coordonnes.items():
        if dico_nom.get(nom_coord[(coords[0][0], coords[0][1])]):
            depart = dico_nom.get(nom_coord[(coords[0][0], coords[0][1])])
        else:
            depart = nom_coord[(coords[0][0], coords[0][1])]

        if dico_nom.get(nom_coord[(coords[-1][0], coords[-1][1])]):
            arrivee = dico_nom.get(nom_coord[(coords[-1][0], coords[-1][1])])
        else:
            arrivee = nom_coord[(coords[-1][0], coords[-1][1])]
        results = trainline.search(
	        departure_station="paris",
	        arrival_station="strasbourg",
	        from_date=date_debut.strftime("%d/%m/%Y %H:%M"),
	        to_date=date_fin.strftime("%d/%m/%Y %H:%M"),
	        bicycle_with_or_without_reservation=True)

def creation_geojson(listes_coordonnes, nom, type_train):
    geojson = {}
    geojson["type"] = "FeatureCollection"
    geojson["features"] = []
    for route, coords in listes_coordonnes.items():
        carac_route = {}
        carac_route["type"] = "Feature"
        carac_route["properties"] = {}
        carac_route["properties"]["id_trajet"] = route
        carac_route["properties"]["nom"] = nom.get(route)

        carac_route["geometry"] = {}
        carac_route["geometry"]["type"] = "LineString"
        carac_route["geometry"]["coordinates"] = []
        for coord in coords:
            carac_route["geometry"]["coordinates"].append(coord)
        geojson["features"].append(carac_route)


    with open('data_{}.geojson'.format(type_train), 'w') as fp:
        json.dump(geojson, fp)

if __name__ == '__main__':
    type_train = "TER"
    coords, nom = recup_gares(type_train)
    creation_geojson(coords, nom, type_train)
    