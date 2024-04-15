
import time

from reading_from_csv import graph_creation
from path_algorithms import astar, astar_for_lanes, astar_improved, dijkstra
from utils import euclidean_distance, manhatann_distance, minutesToTime, print_path_info

def algorithm_handler(graph, stop_coordinates ,optimization_value, start_stop, end_stop, start_time_for_dijkstra):
    if(optimization_value == 'p'):
        performance_mesurment_start = time.perf_counter()
        path = astar(graph, start_stop, end_stop, start_time_for_dijkstra, euclidean_distance, stop_coordinates)
        execution_time = time.perf_counter() - performance_mesurment_start
        print_path_info(path)

    elif(optimization_value == 't'):
        performance_mesurment_start = time.time()
        path = astar_for_lanes(graph, start_stop, end_stop, start_time_for_dijkstra, manhatann_distance, stop_coordinates)
        execution_time = time.time() - performance_mesurment_start
        print_path_info(path)
    else:
        print('please put correct value')


def main():
    filename = "connection_graph.csv"


    print('Reading part')
    performance_mesurment_start = time.time()
    graph, stop_coordinates = graph_creation(filename)
    performance_mesurment_end = time.time()

    execution_time = performance_mesurment_end - performance_mesurment_start
    print(f"Execution time: {execution_time} seconds")
    
    # shows keeping one line
    start_stop = "EPI"  
    end_stop = "Strzegomska (krzyżówka)"  

    # start_stop = "Koszarowa"  
    # end_stop = "GALERIA DOMINIKAŃSKA"  
     
    # start_stop = "Piramowicza (Kampus Biskupin)"  
    # end_stop = "pl. Legionów"  

    # start_stop = "Oboźna"  
    # end_stop = "Parafialna"  

    start_time_for_dijkstra = "10:31"  


    print("Start \n")

    print("Task 1.1 - Dijkstra's Algorithm")
    performance_mesurment_start = time.perf_counter()
    path = dijkstra(graph, start_stop, end_stop, start_time_for_dijkstra)
    execution_time = time.perf_counter() - performance_mesurment_start
    
    print_path_info(path)
    print(f"Execution time: {execution_time} seconds")

    print("\nTask 1.2 - A* Algorithm")

    performance_mesurment_start = time.perf_counter()
    path = astar(graph, start_stop, end_stop, start_time_for_dijkstra, euclidean_distance, stop_coordinates)
    execution_time = time.perf_counter() - performance_mesurment_start
    
    print_path_info(path)
    print(f"Execution time: {execution_time} seconds")
    
    print("\nTask 1.3 - A* Algorithm optimisation")
    
    performance_mesurment_start = time.time()
    path = astar_improved(graph, start_stop, end_stop, start_time_for_dijkstra, manhatann_distance, stop_coordinates)
    execution_time = time.time() - performance_mesurment_start

    print_path_info(path)
    print(f"Execution time: {execution_time} seconds")

    print("\nTask 1.4 - A* Algorithm for minimum lane changing")

    performance_mesurment_start = time.time()
    path = astar_for_lanes(graph, start_stop, end_stop, start_time_for_dijkstra, manhatann_distance, stop_coordinates)
    execution_time = time.time() - performance_mesurment_start

    print_path_info(path)
    print(f"Execution time: {execution_time} seconds")

    # Ask the user for their name
    type_of_optimisation = input("Do you want to optimize based on optimization criterion: value t denotes travel time minimization, value p means minimization of the number of transfers (t/p)? ")
    point_a=input("Choose the point A:")
    point_b=input("Choose the point B:")
    chosen_time = input("choose time in HH:MM format")

    # algorithm_handler(graph,stop_coordinates,type_of_optimisation,point_a,point_b,chosen_time)

if __name__ == "__main__":
    main()

