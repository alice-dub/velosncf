import csv
import json
import pandas as pd

element = []
type_fichier = "stop_times"

data = pd.read_csv('{}/{}.txt'.format("TER", type_fichier))

def stop_id():
    stop_id_unique = data['stop_id'].unique().tolist()
    for id in stop_id_unique:
        data_id = data[data['stop_id'] == id]
        i = 0
        with open('id_stops/{}.json'.format(id), 'wt', encoding='utf8') as fp:
            data_id.to_json(fp, orient="records", force_ascii=False)


def trips_id():
    stop_id_unique = data['trip_id'].unique().tolist()
    for id in stop_id_unique:
        data_id = data[data['trip_id'] == id]
        i = 0
        with open('id_trips/{}.json'.format(id), 'wt', encoding='utf8') as fp:
            data_id.to_json(fp, orient="records", force_ascii=False)

trips_id()
