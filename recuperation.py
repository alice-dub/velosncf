import csv, sys

csv.field_size_limit(sys.maxsize)

lignes_trace = {}


#### Recuperation des gares apparantees a chaque ligne de train 

with open('formes-des-lignes-du-rfn.csv') as forme:
   with open('lignes-par-statut.csv') as nom: 
        with open('liste-des-gares.csv') as gare:
            forme_reader = list(csv.reader(forme, delimiter=';'))
            nom_reader = csv.reader(nom, delimiter=';')
            gare_reader = list(csv.reader(gare, delimiter=';'))
            i = 0
            for row in forme_reader:
                for row_3 in gare_reader:
                    if row_3[4] == row[2]:
                        if not row[2] in lignes_trace:
                            lignes_trace[row[2]] = set()
                        lignes_trace[row[2]].add(row_3[1])

print(lignes_trace)

#### 