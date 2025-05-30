# TSP Solver z użyciem Ant Colony Optimization (ACO) i 2-opt

Projekt zaliczeniowy z Optymalizacji Kombinatorycznej na Politechnice Poznańskiej. Celem projektu było zaimplementowanie metaheurystyki ACO do rozwiązania problemu komiwojażera (TSP) oraz porównanie jej działania z algorytmem zachłannym (Greedy) i ulepszeniem 2-opt.

## Zawartość projektu

- `tsp_aco_project.py` – główna implementacja ACO i testy na losowych instancjach.
- `benchmark_runner.py` – testy na benchmarkach TSPLIB + wykresy błędów względnych.
- `instance_loader.py` – wczytywanie instancji w formacie `.txt` i `.tsp`.
- `data/` – folder z instancjami TSP (`berlin52.tsp`, `tsp250.txt` itd.).
- `Sprawozdanie.docx` - sprawozdanie zawierające analize algorytmów (`krótki opis algorytmu`, `wykresy`, `pseudokod`, `tabela instancji rankingowych`).

## Technologie

- Python 3.11+
- NumPy
- Matplotlib

## Funkcje i analiza

ACO inicjalizowane trasą z algorytmu zachłannego.

Porównanie długości tras:

- `Greedy`

- `ACO`

- `ACO + 2-opt`

Obliczanie błędów względnych dla benchmarków (berlin52, bier127, tsp250, tsp500, tsp1000, itd.).

Wykresy:

- `Porównanie ACO vs Greedy dla instancji losowych (15 punktów).`

- `Błąd względny dla benchmarków vs wartości optymalne.`

## Algorytmy

- `ACO (Ant Colony Optimization) – metaheurystyka symulująca zachowanie kolonii mrówek.`

- `Greedy (Nearest Neighbour) – szybka heurystyka do generowania trasy początkowej.`

- `2-opt – lokalna optymalizacja trasy poprzez zamianę dwóch krawędzi.`

## Benchmarki

W projekcie użyto instancji z biblioteki TSPLIB oraz instancji losowych:

berlin52.tsp, bier127.tsp, att48.tsp, a280.tsp ...

tsp250.txt, tsp500.txt, tsp1000.txt

## Źródła

GeeksForGeeks – Ant Colony Optimization

TSPLIB Benchmarki

## Autor

Wiktor Opieliński, Informatyka niestacjonarna – 2 rok
Politechnika Poznańska
