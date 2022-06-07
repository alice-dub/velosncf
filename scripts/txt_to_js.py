import csv
import json

element = []
type_fichier = "stop_times"

with open('{}/{}.txt'.format("TER", type_fichier), encoding='utf-8') as stop:
    stop_reader = csv.reader(stop, delimiter=',')
    i = 0
    for row in stop_reader:
        if i == 0:
            keys = row
        else:
            dico = {}
            for i in range(len(row)):
                dico[keys[i]] = row[i].replace("'\'", " ")
            element.append(dico)
        i += 1

with open('js_{}.json'.format(type_fichier), 'wt', encoding='utf8') as fp:
    json.dump(element, fp, ensure_ascii=False)