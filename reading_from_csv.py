import csv

from utils import timeToMinutes

INDEX = 0
COMPANY = 1
LINE = 2
DEPARTURE_TIME = 3
ARRIVAL_TIME = 4
START_STOP = 5
END_STOP = 6
START_STOP_LAT = 7
START_STOP_LON = 8
END_STOP_LAT = 9
END_STOP_LON = 10


def graph_creation(filename):
    graph = {}
    stop_coordinates = {}
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row

        for row in csvreader:
            start_stop = row[START_STOP]
            end_stop = row[END_STOP]
            line = row[LINE]
            departure_time = timeToMinutes(row[DEPARTURE_TIME])
            arrival_time = timeToMinutes(row[ARRIVAL_TIME])
            company = row[COMPANY]
            # Using lat and lon if needed later
            start_stop_lat, start_stop_lon = row[START_STOP_LAT], row[START_STOP_LON]
            end_stop_lat, end_stop_lon = row[END_STOP_LAT], row[END_STOP_LON]

            if start_stop not in graph:
                graph[start_stop] = {}
            if end_stop not in graph[start_stop]:
                graph[start_stop][end_stop] = {}
            if line not in graph[start_stop][end_stop]:
                graph[start_stop][end_stop][line] = []

            # Append this specific trip information
            graph[start_stop][end_stop][line].append({
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'company': company,
                'start_stop_lat': start_stop_lat,
                'start_stop_lon': start_stop_lon,
                'end_stop_lat': end_stop_lat,
                'end_stop_lon': end_stop_lon
            })
            if start_stop not in stop_coordinates:
                stop_coordinates[start_stop] = {
                    'start_stop_lat': start_stop_lat,
                    'start_stop_lon': start_stop_lon,
                }

        return graph, stop_coordinates


