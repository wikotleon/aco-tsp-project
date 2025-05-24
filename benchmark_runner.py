
from tsp_aco_project import (
    create_distance_matrix,
    nearest_neighbour,
    tour_length,
    two_opt,
    AntColonyTSPWithGreedyStart,
    calculate_lower_bound
)
from instance_loader import load_instance
import os

def run_benchmark_tests():
    print("Running tests on all .tsp and .txt instances in folder...")
    for filename in sorted(os.listdir(".")):
        if filename.endswith(".tsp") or filename.endswith(".txt"):
            try:
                cities = load_instance(filename)
                if len(cities) == 0:
                    raise ValueError("Plik nie zawiera współrzędnych.")
                dist_matrix = create_distance_matrix(cities)

                greedy_tour = nearest_neighbour(dist_matrix)
                greedy_len = tour_length(greedy_tour, dist_matrix)

                aco = AntColonyTSPWithGreedyStart(dist_matrix, greedy_tour, n_ants=20, n_iter=100)
                aco_tour, aco_len = aco.run()

                aco_tour_2opt = two_opt(aco_tour, dist_matrix)
                aco_len_2opt = tour_length(aco_tour_2opt, dist_matrix)

                lower_bound = calculate_lower_bound(dist_matrix)

                print(f"--- {filename} ---")
                print(f"Lower Bound: {lower_bound:.2f}")
                print(f"Greedy: {greedy_len:.2f} -> Error: {(greedy_len - lower_bound) / lower_bound * 100:.2f}%")
                print(f"ACO: {aco_len:.2f} -> Error: {(aco_len - lower_bound) / lower_bound * 100:.2f}%")
                print(f"ACO + 2-opt: {aco_len_2opt:.2f} -> Error: {(aco_len_2opt - lower_bound) / lower_bound * 100:.2f}%\n")

            except Exception as e:
                print(f"Failed to process {filename}: {e}\n")

if __name__ == "__main__":
    run_benchmark_tests()
