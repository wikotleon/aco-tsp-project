
import numpy as np
import random
from typing import List

# generator TSP
def generate_cities(n: int, seed: int = 42):
    np.random.seed(seed)
    return np.random.rand(n, 2) * 100

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

def create_distance_matrix(cities: np.ndarray):
    n = len(cities)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = euclidean_distance(cities[i], cities[j])
    return dist_matrix

# Nearest Neighbour Heurystyka
def nearest_neighbour(dist_matrix: np.ndarray):
    n = len(dist_matrix)
    unvisited = set(range(1, n))
    tour = [0]
    while unvisited:
        last = tour[-1]
        next_city = min(unvisited, key=lambda x: dist_matrix[last][x])
        tour.append(next_city)
        unvisited.remove(next_city)
    tour.append(0)
    return tour

def tour_length(tour: List[int], dist_matrix: np.ndarray):
    return sum(dist_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1))

# Ant Colony Optimization zaczynajaca od pozycji algorytmu zachłannego
class AntColonyTSPWithGreedyStart:
    def __init__(self, dist_matrix, greedy_tour, n_ants=10, n_iter=100, alpha=1, beta=5, evaporation=0.5, Q=100):
        self.dist_matrix = dist_matrix
        self.n = len(dist_matrix)
        self.n_ants = n_ants
        self.n_iter = n_iter
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        self.Q = Q
        self.pheromone = np.ones((self.n, self.n))
        self.best_tour = greedy_tour
        self.best_length = tour_length(greedy_tour, dist_matrix)

    def run(self):
        for _ in range(self.n_iter):
            all_tours = []
            for _ in range(self.n_ants):
                tour = self.construct_tour()
                length = tour_length(tour, self.dist_matrix)
                if length < self.best_length:
                    self.best_length = length
                    self.best_tour = tour
                all_tours.append((tour, length))
            self.update_pheromone(all_tours)
        return self.best_tour, self.best_length

    def construct_tour(self):
        tour = [random.randint(0, self.n - 1)]
        unvisited = set(range(self.n)) - {tour[0]}
        while unvisited:
            current = tour[-1]
            probabilities = []
            candidates = []
            for city in unvisited:
                distance = self.dist_matrix[current][city]
                if distance == 0:
                    continue
                pher = self.pheromone[current][city] ** self.alpha
                visibility = (1 / distance) ** self.beta
                candidates.append(city)
                probabilities.append(pher * visibility)
            probabilities = np.array(probabilities)
            if probabilities.sum() == 0 or len(candidates) == 0:
                break
            probabilities /= probabilities.sum()
            next_city = random.choices(candidates, weights=probabilities)[0]
            tour.append(next_city)
            unvisited.remove(next_city)
        tour.append(tour[0])
        return tour

    def update_pheromone(self, all_tours):
        self.pheromone *= (1 - self.evaporation)
        for tour, length in all_tours:
            for i in range(len(tour) - 1):
                a, b = tour[i], tour[i+1]
                self.pheromone[a][b] += self.Q / length
                self.pheromone[b][a] += self.Q / length

# 2-opt optymalizacja
def two_opt(tour, dist_matrix):
    best = tour
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best) - 1):
                if j - i == 1:
                    continue
                new_tour = best[:i] + best[i:j][::-1] + best[j:]
                if tour_length(new_tour, dist_matrix) < tour_length(best, dist_matrix):
                    best = new_tour
                    improved = True
        tour = best
    return best

# Obliczanie Dolnej Granicy
def calculate_lower_bound(dist_matrix):
    n = len(dist_matrix)
    bound = 0
    for i in range(n):
        sorted_edges = sorted(dist_matrix[i][j] for j in range(n) if i != j)
        bound += sorted_edges[0] + sorted_edges[1]
    return bound / 2

