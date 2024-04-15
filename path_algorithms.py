import heapq
from utils import minutesToTime, timeToMinutes

cost_index = 0
PREV_INDEX = 1
DEP_TIME_INDEX = 2
ARR_TIME_INDEX = 3
LINE_INDEX = 4


def dijkstra(graph, start, end, start_time):
    start_time_minutes = timeToMinutes(start_time)
    queue = [(0, start, None, start_time_minutes, start_time_minutes, None)]  # Initialize with total cost, current stop, etc.
    visited = {} 
    while queue:
        cost, current, prev, dep_time, arr_time, line = heapq.heappop(queue)
        if current in visited:
            continue
        visited[current] = (cost, prev, dep_time, arr_time, line)

        if current == end:
            break 

        for next_stop, lines in graph.get(current, {}).items():
            if next_stop not in graph:
                continue
            for line, trips in lines.items():
                for trip in trips:
                    if trip['departure_time'] >= arr_time: 
                        wait_time = trip['departure_time'] - arr_time
                        travel_time = trip['arrival_time'] - trip['departure_time']
                        new_cost = cost + wait_time + travel_time
                        if next_stop not in visited or new_cost < visited[next_stop][0]:
                            heapq.heappush(queue, (new_cost, next_stop, current, trip['departure_time'], trip['arrival_time'], line))


# Path reconstruction
    path = []
    current = end
    while current:
        if current in visited:
            node = visited[current]  # node structure: (cost, prev, dep_time, arr_time, line)
            path.append((node[PREV_INDEX], current, node[ARR_TIME_INDEX], node[DEP_TIME_INDEX], node[LINE_INDEX])) 
            current = node[PREV_INDEX]
        else:
            break
    path.reverse()


    return path

def astar(graph, start, end, start_time, distance_function, stop_coordinates):
    start_time_minutes = timeToMinutes(start_time)
    end_lat, end_lon = float(stop_coordinates[end]['start_stop_lat']), float(stop_coordinates[end]['start_stop_lon']) # Destination coordinates

    queue = [(0, start, None, start_time_minutes, start_time_minutes, None, 0)]  # Initial heuristic is 0
    visited = {}
    while queue:
        cost, current, prev, dep_time, arr_time, line, _ = heapq.heappop(queue)
        if current in visited:
            continue
        visited[current] = (cost, prev, dep_time, arr_time, line)

        if current not in graph:
            continue

        if current == end:
            break

        current_lat, current_lon = float(stop_coordinates[current]['start_stop_lat']), float(stop_coordinates[current]['start_stop_lon'])  # Current coordinates
        heuristic = distance_function(current_lat, current_lon, end_lat, end_lon)  # Calculate heuristic

        for next_stop, lines in graph.get(current, {}).items():
            if next_stop not in graph:
                continue
            next_lat, next_lon = float(stop_coordinates[next_stop]['start_stop_lat']), float(stop_coordinates[next_stop]['start_stop_lon'])

            # Calculate heuristic for the next_stop towards the end
            next_stop_heuristic = distance_function(next_lat, next_lon, end_lat, end_lon)*10

            for line, trips in lines.items():
                for trip in trips:
                    if trip['departure_time'] >= arr_time:
                        wait_time = trip['departure_time'] - arr_time
                        travel_time = trip['arrival_time'] - trip['departure_time']
                        new_cost = cost + wait_time + travel_time
                        total_cost = new_cost + next_stop_heuristic
                        heapq.heappush(queue, (total_cost, next_stop, current, trip['departure_time'], trip['arrival_time'], line, next_stop_heuristic))
# Path reconstruction

    path = []
    current = end
    while current:
        if current in visited:
            node = visited[current]  # node structure: (cost, prev, dep_time, arr_time, line)
            path.append((node[PREV_INDEX], current, node[ARR_TIME_INDEX], node[DEP_TIME_INDEX], node[LINE_INDEX]))  # Adjusted indices
            current = node[PREV_INDEX]
        else:
            break
    path.reverse()

    return path

def astar_improved(graph, start, end, start_time, distance_function, stop_coordinates):
    start_time_minutes = timeToMinutes(start_time)
    end_lat, end_lon = float(stop_coordinates[end]['start_stop_lat']), float(stop_coordinates[end]['start_stop_lon']) # Destination coordinates

    queue = [(0, start, None, start_time_minutes, start_time_minutes, None, 0)]  # Initial heuristic is 0
    visited = {}
    while queue:
        cost, current, prev, dep_time, arr_time, line, _ = heapq.heappop(queue)
        if current in visited:
            continue
        visited[current] = (cost, prev, dep_time, arr_time, line)

        if current == end:
            break

        current_lat, current_lon = float(stop_coordinates[current]['start_stop_lat']), float(stop_coordinates[current]['start_stop_lon'])  # Current coordinates
        heuristic = distance_function(current_lat, current_lon, end_lat, end_lon)  # Calculate heuristic

        for next_stop, lines in graph.get(current, {}).items():
            if next_stop not in graph:
                continue
            next_lat, next_lon = float(stop_coordinates[next_stop]['start_stop_lat']), float(stop_coordinates[next_stop]['start_stop_lon'])

            # Calculate heuristic for the next_stop towards the end
            next_stop_heuristic = distance_function(next_lat, next_lon, end_lat, end_lon)*100

            for line, trips in lines.items():
                
                for trip in trips:
                    if trip['departure_time'] >= arr_time:
                        wait_time = trip['departure_time'] - arr_time
                        travel_time = trip['arrival_time'] - trip['departure_time']
                        new_cost = cost + wait_time + travel_time
                        # Use next_stop's heuristic for total cost calculation
                        total_cost = new_cost + next_stop_heuristic
                        heapq.heappush(queue, (total_cost, next_stop, current, trip['departure_time'], trip['arrival_time'], line, next_stop_heuristic))

# Path reconstruction
    path = []
    current = end
    while current:
        if current in visited:
            node = visited[current]  # node structure: (cost, prev, dep_time, arr_time, line)
            path.append((node[PREV_INDEX], current, node[ARR_TIME_INDEX], node[DEP_TIME_INDEX], node[LINE_INDEX]))  # Adjusted indices
            current = node[PREV_INDEX]
        else:
            break
    path.reverse()

    return path

def astar_for_lanes(graph, start, end, start_time, distance_function, stop_coordinates):
    start_time_minutes = timeToMinutes(start_time)
    end_lat, end_lon = float(stop_coordinates[end]['start_stop_lat']), float(stop_coordinates[end]['start_stop_lon'])

    queue = [(0, 0, start, None, start_time_minutes, start_time_minutes, None)]  # (line_changes, total_travel_time, current, ...)
    visited = {}
    while queue:
        # Extract line_changes and total_travel_time from the queue
        line_changes, total_travel_time, current, prev, dep_time, arr_time, prev_line = heapq.heappop(queue)
        if current in visited:
            continue
        visited[current] = (line_changes, total_travel_time, prev, dep_time, arr_time, prev_line)
        
        if current not in graph:
            continue
        
        if current == end:
            break

        current_lat, current_lon = float(stop_coordinates[current]['start_stop_lat']), float(stop_coordinates[current]['start_stop_lon'])
        heuristic = distance_function(current_lat, current_lon, end_lat, end_lon)  # Used for priority but does not affect cost

        for next_stop, lines in graph.get(current, {}).items():
            if next_stop not in graph:
                continue
            next_lat, next_lon = float(stop_coordinates[next_stop]['start_stop_lat']), float(stop_coordinates[next_stop]['start_stop_lon'])

            for next_line, trips in lines.items():
                for trip in trips:
                    if trip['departure_time'] >= arr_time:
                        wait_time = trip['departure_time'] - arr_time
                        travel_time = trip['arrival_time'] - trip['departure_time']
                        # Determine if changing lines
                        if prev_line is None or prev_line == next_line:
                            new_line_changes = line_changes
                        else:
                            new_line_changes = line_changes + 1
                        new_total_travel_time = total_travel_time + wait_time + travel_time
                        
                        # Push new state to the queue with updated costs
                        heapq.heappush(queue, (new_line_changes, new_total_travel_time, next_stop, current, trip['departure_time'], trip['arrival_time'], next_line))
# Path reconstruction

    path = []
    current = end
    while current:
        if current in visited:
            node = visited[current]
            path.append((node[PREV_INDEX+1], current, node[ARR_TIME_INDEX+1], node[DEP_TIME_INDEX+1], node[LINE_INDEX+1]))  # Adjusted indices
            current = node[PREV_INDEX+1]
        else:
            break
    path.reverse()

    return path
