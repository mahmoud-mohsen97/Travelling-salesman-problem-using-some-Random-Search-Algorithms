import csv
import math
import random
import numpy as np
import matplotlib.pyplot as plt


class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x},{self.y})'


def calculate_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def generate_distance_matrix(data):
    n = len(data)
    distance_matrix = {i: {j: 0 for j in range(n)} for i in range(n)}

    for i, (name1, (x1, y1)) in enumerate(data.items()):
        for j, (name2, (x2, y2)) in enumerate(data.items()):
            distance = calculate_distance((x1, y1), (x2, y2))
            distance_matrix[i][j] = distance

    return distance_matrix


def get_nearest_neighbor(city, matrix, visited):
    n = len(matrix)
    min_distance = np.inf
    nearest_neighbor = city

    for i in range(n):
        if i == city or i in visited:
            continue
        distance = matrix[city][i]

        if distance < min_distance:
            min_distance = distance
            nearest_neighbor = i

    return min_distance, nearest_neighbor

def plot_path(path, city_data):
    x = [city_data[str(i+1)][0] for i in path] + [city_data[str(path[0]+1)][0]]
    y = [city_data[str(i+1)][1] for i in path] + [city_data[str(path[0]+1)][1]]
    fig, ax = plt.subplots()
    ax.plot(x, y, '-o')
    ax.set_title('Path by N-N')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.show()


if __name__ == '__main__':

    city_data = {}

    with open('15-Points.csv') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name = row[2]
            x = float(row[0])
            y = float(row[1])
            city = City(name, x, y)
            city_data[name] = (city.x, city.y)  # add instance to dictionary using city name as key

    visited = set()
    start = 0
    distance_matrix = generate_distance_matrix(city_data)
    total_cost = 0
    path = [start]

    while True:
        min_distance, nearest_neighbor = get_nearest_neighbor(start, distance_matrix, visited)
        visited.add(nearest_neighbor)
        total_cost += min_distance
        if len(visited) == len(city_data):
            break
        start = nearest_neighbor
        path.append(nearest_neighbor)

    print(f"The Total Cost is : {total_cost} ")
    print(f"THE Path is {path} ")
    plot_path(path, city_data)

