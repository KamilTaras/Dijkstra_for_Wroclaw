import math


def timeToMinutes(time_in_string: str) -> int:
    time = time_in_string.split(":")
    str_hours_to_minutes = int(time[0])*60
    str_minutes_to_minutes = int(time[1])
    return str_hours_to_minutes + str_minutes_to_minutes

def minutesToTime(minutes: int) -> str:
    hours = minutes // 60 
    mins = minutes % 60  
    return f"{hours:02}:{mins:02}"

def euclidean_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def manhatann_distance(lat1, lon1, lat2, lon2):
    return abs((lat1 - lat2)) +  abs(lon1 - lon2)


def print_path_info(path):
    print(f"{'From':<50} - {'To':<50} - {'Start Time':<10} - {'Arrival Time':<10} - {'Line':<5}")
    print("-" * 150)
    
    for step in path:
        from_location = step[0] if step[0] is not None else 'N/A'
        to_location = step[1] if step[1] is not None else 'N/A'
        start_time = minutesToTime(step[3]) if step[3] is not None else 'N/A'
        line = step[4] if step[4] is not None else 'N/A'
        arrival_time = minutesToTime(step[2]) if step[2] is not None else 'N/A'
        
        print(f"{from_location:<50} - {to_location:<50} - {start_time:<12} - {arrival_time:<12} - {line:<5}")
