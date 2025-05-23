
import numpy as np

def parse_tsplib(filename):
    coords = []
    with open(filename, 'r') as file:
        section = False
        for line in file:
            line = line.strip()
            if line.startswith("NODE_COORD_SECTION"):
                section = True
                continue
            if section:
                if line == "EOF":
                    break
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        x = float(parts[1])
                        y = float(parts[2])
                        coords.append((x, y))
                    except ValueError:
                        continue
    return np.array(coords)

def parse_simple_txt(filename):
    coords = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 3:
                try:
                    x = float(parts[1])
                    y = float(parts[2])
                    coords.append((x, y))
                except ValueError:
                    continue
    return np.array(coords)

def load_instance(filename):
    if filename.lower().endswith('.tsp'):
        return parse_tsplib(filename)
    elif filename.lower().endswith('.txt'):
        return parse_simple_txt(filename)
    else:
        raise ValueError("Unsupported file format: must be .tsp or .txt")
