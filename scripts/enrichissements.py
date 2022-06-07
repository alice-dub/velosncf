import pandas as pd

data_stop = pd.read_csv('{}/{}.txt'.format("TER", "stops"))
data = pd.read_csv('{}/{}.txt'.format("TER", "stop_times"))
data_trips = pd.read_csv('{}/{}.txt'.format("TER", "trips"))
data_routes = pd.read_csv('{}/{}.txt'.format("TER", "routes"))


data = pd.merge(data, data_stop, on="stop_id")
data = pd.merge(data, data_trips, on="trip_id")
data = pd.merge(data, data_routes, on="route_id")
data = data[data["route_type"] == 2]

def stop_id():
    stop_id_unique = data['stop_name'].unique().tolist()
    for id in stop_id_unique:
        data_id = data[data['stop_name'] == id]
        i = 0
        with open('id_stops/{}.json'.format(id.replace("/", "_")), 'wt', encoding='utf8') as fp:
            data_id.to_json(fp, orient="records", force_ascii=False)


def trips_id():
    stop_id_unique = data['trip_id'].unique().tolist()
    for id in stop_id_unique:
        data_id = data[data['trip_id'] == id]
        i = 0
        with open('id_trips/{}.json'.format(id), 'wt', encoding='utf8') as fp:
            data_id.to_json(fp, orient="records", force_ascii=False)

stop_id()
trips_id()
