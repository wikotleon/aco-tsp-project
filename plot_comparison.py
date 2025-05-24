from tsp_aco_project import generate_cities, create_distance_matrix, nearest_neighbour, tour_length, two_opt, AntColonyTSPWithGreedyStart
import matplotlib.pyplot as plt

def porownaj_greedy_aco_2opt_losowe(n_instancji=15, n_miast=30):
    greedy_dlugosci = []
    aco_2opt_dlugosci = []

    for seed in range(n_instancji):
        cities = generate_cities(n_miast, seed=seed)
        dist_matrix = create_distance_matrix(cities)

        greedy_tour = nearest_neighbour(dist_matrix)
        greedy_len = tour_length(greedy_tour, dist_matrix)

        aco = AntColonyTSPWithGreedyStart(dist_matrix, greedy_tour, n_ants=20, n_iter=100)
        aco_tour, _ = aco.run()

        aco_2opt_tour = two_opt(aco_tour, dist_matrix)
        aco_2opt_len = tour_length(aco_2opt_tour, dist_matrix)

        greedy_dlugosci.append(greedy_len)
        aco_2opt_dlugosci.append(aco_2opt_len)

    # Wykres
    x = list(range(1, n_instancji + 1))
    plt.figure(figsize=(10, 6))
    plt.plot(x, greedy_dlugosci, marker='o', label="Greedy")
    plt.plot(x, aco_2opt_dlugosci, marker='o', label="ACO + 2-opt")
    plt.fill_between(x, greedy_dlugosci, aco_2opt_dlugosci, color='lightblue', alpha=0.4)
    plt.xlabel("Numer instancji (losowy seed)")
    plt.ylabel("Długość trasy")
    plt.title("Porównanie długości tras: Greedy vs ACO + 2-opt (losowe instancje)")
    plt.grid(True)
    plt.legend()
    plt.xticks(list(range(1, n_instancji + 1)))
    plt.savefig("porownanie_greedy_aco_2opt_losowe.png")
    plt.close()

    print("Wygenerowano wykres: porownanie_greedy_aco_2opt_losowe.png")


if __name__ == "__main__":
    porownaj_greedy_aco_2opt_losowe()
