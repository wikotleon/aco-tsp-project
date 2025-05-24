
from tsp_aco_project import (
    create_distance_matrix,
    nearest_neighbour,
    tour_length,
    two_opt,
    AntColonyTSPWithGreedyStart
)
from instance_loader import load_instance
import matplotlib.pyplot as plt
import os

benchmark_instances = {
    "berlin52.tsp": 7542,
    "bier127.tsp": 118282,
    "a280.tsp": 2579,
    "st70.tsp": 675,
    "pr76.tsp": 108159,
    "eil101.tsp": 629,
    "ch130.tsp": 6110,
    "tsp250.txt": 12526,
    "tsp500.txt": 84577,
    "tsp1000.txt": 23979
}

def run_benchmark_tests():
    print("Uruchamianie testów dla wszystkich instancji .tsp i .txt w folderze...")
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

                if filename in benchmark_instances:
                    optimum = benchmark_instances[filename]
                    print(f"--- {filename} ---")
                    print(f"Wartość optymalna: {optimum}")
                    print(f"Greedy: {greedy_len:.2f} -> Błąd względny: {(greedy_len - optimum) / optimum * 100:.2f}%")
                    print(f"ACO: {aco_len:.2f} -> Błąd względny: {(aco_len - optimum) / optimum * 100:.2f}%")
                    print(f"ACO + 2-optymalizacja: {aco_len_2opt:.2f} -> Błąd względny: {(aco_len_2opt - optimum) / optimum * 100:.2f}%\n")
                else:
                    print(f"--- {filename} ---")
                    print(f"Greedy: {greedy_len:.2f}")
                    print(f"ACO: {aco_len:.2f}")
                    print(f"ACO + 2-optymalizacja: {aco_len_2opt:.2f}\n")

            except Exception as e:
                print(f"Nie udało się przetworzyć {filename}: {e}\n")

# Wykres
def plot_relative_errors(instances_dict):
    instance_names = []
    relative_errors = []

    for filename, optimum in instances_dict.items():
        try:
            cities = load_instance(filename)
            if len(cities) == 0:
                raise ValueError("Plik nie zawiera współrzędnych.")
            dist_matrix = create_distance_matrix(cities)

            greedy_tour = nearest_neighbour(dist_matrix)
            aco = AntColonyTSPWithGreedyStart(dist_matrix, greedy_tour, n_ants=20, n_iter=30)
            aco_tour, _ = aco.run()

            aco_tour_2opt = two_opt(aco_tour, dist_matrix)
            aco_len_2opt = tour_length(aco_tour_2opt, dist_matrix)

            error = ((aco_len_2opt - optimum) / optimum) * 100
            instance_names.append(filename.replace(".tsp", "").replace(".txt", ""))
            relative_errors.append(error)

        except Exception as e:
            print(f"Nie udało się przetworzyć {filename}: {e}")

    plt.figure(figsize=(12, 6))
    bars = plt.bar(instance_names, relative_errors, color='lightcoral')
    plt.axhline(0, color='black', linewidth=0.8)
    plt.title("Błąd względny ACO + 2-optymalizacja względem wartości optymalnej")
    plt.ylabel("Błąd względny [%]")
    plt.xlabel("Instancja")
    plt.xticks(rotation=45)
    for bar, val in zip(bars, relative_errors):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{val:.1f}%", 
                 ha='center', va='bottom', fontsize=8)
    plt.tight_layout()
    plt.savefig("blad_wzgledny_benchmarki.png")
    plt.close()
    print("Wygenerowano wykres: blad_wzgledny_benchmarki.png")

if __name__ == "__main__":
    run_benchmark_tests() # do testow
    plot_relative_errors(benchmark_instances) # do wykresu
