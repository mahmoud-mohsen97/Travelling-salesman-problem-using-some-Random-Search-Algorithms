import csv
import random
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self):
        return f'<City:\tname: {self.name},\tx: {self.x},\ty: {self.y}>'

class AntPath:
    def __init__(self, path):
        self.path = path
        self.fitness = -1
        self.cost = -1

    def __repr__(self):
        return f'<Tour:\tfitness: {self.fitness},\tPath:\n{self.path}>'


def calculate_distance(city1, city2):
    return np.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)

def calculate_cost(AntPath, distance_matrix):
    total_cost = 0
    path = AntPath.path
    n = len(path)
    # Calculate the cost of traversing the path in the Ant Path.
    for i in range(1, n):
        total_cost += distance_matrix[path[i].name][path[i - 1].name]
    total_cost += distance_matrix[path[0].name][path[-1].name]
    return total_cost

def generate_distance_matrix(cities):
    n = len(cities)
    distance_matrix = {}
    # Iterate over each city and calculate its distance to all other cities.
    for city1 in cities:
        distance_matrix[city1.name] = {}
        for city2 in cities:
            distance_matrix[city1.name][city2.name] = calculate_distance(city1, city2)
    return distance_matrix

def generat_population(lst_cities, pop_size, dist_mat):
    population = []

    # create random Ant Path
    for i in range(pop_size):
        path = lst_cities.copy()
        random.shuffle(path)

        chrom = AntPath(path)

        # calculate the cost for the created chrom path
        cost = calculate_cost(chrom, dist_mat)
        chrom.cost = cost
        chrom.fitness = 1 / cost

        # add the chrom to the population
        population.append(chrom)

    return population


def update_phromone_matrix(phormone_mat, pop, roo=0.5):
    for key, dic in phormone_mat.items():
        nw = {key: val * (1 - roo) for key, val in dic.items()}
        phormone_mat[key] = nw

    new_phormone_mat = phormone_mat
    # sum each partial path to the population matrix
    for ant in pop:
        lst = ant.path
        path_fit = ant.fitness

        n = len(lst)
        for i in range(1, n):
            # add the ants saved pheromones in the previous step to phormone matrix
            phormone_mat[lst[i].name][lst[i - 1].name] += path_fit
            phormone_mat[lst[i - 1].name][lst[i].name] += path_fit

        phormone_mat[lst[0].name][lst[-1].name] += path_fit
        phormone_mat[lst[-1].name][lst[0].name] += path_fit

    return phormone_mat


def initial_phromone_matrix(data, initial_pop):
    n = len(data)
    phormone_mat = {}

    for point in data:
        key = point.name
        phormone_mat[key] = {}
    for point in data:
        key = point.name
        # for each data point calc the distance between it and all the other points
        for j in range(n):
            p2 = data[j]
            c = p2.name
            phormone_mat[key][c] = 0.0001
    # for intially it = the update
    phormone_mat = update_phromone_matrix(phormone_mat, initial_pop, roo=0.9999)
    return phormone_mat


def pick_move(data, city, phormone_mat, dist_mat, vis, alpha=1, beta=3):

    prop_city_all = {}
    prop_sum = 0
    # calculate next step
    for c in data:
        if c.name not in vis:
            prop = (phormone_mat[city.name][c.name] ** alpha) * ((1.0 / dist_mat[city.name][c.name]) ** beta)
            prop_city_all[c.name] = prop
            prop_sum += prop

    # after getting the whole probabilites divid them by their sum
    for c in prop_city_all:
        prop_city_all[c] /= prop_sum

    # select max probability
    selected = max(prop_city_all, key=prop_city_all.get)
    # print("after", vis)


    # find which city with the max probability
    selected_city = None
    for c in data:
        if c.name == selected:
            selected_city = c

    return selected_city


def construct_solution(data, dist_mat, phormone_mat, alpha, beta, size):
    n = len(data)
    pop = []
    # construct a solution of size the intial pop that contains 50 croms
    for i in range(size):
        vis = {}
        # chose a random start C0
        C0 = random.randrange(n - 1)
        city = data[C0]
        path = [city]
        vis[city.name] = 1

        # loop until construct one path of length n
        while len(vis) < n:

            # choose the next city in crom according to the probablity equation
            nxt = pick_move(data, city, phormone_mat, dist_mat, vis, alpha, beta)

            # append city into path and mark it in the visited list
            path.append(nxt)
            vis[nxt.name] = 1
            # update the current city
            city = nxt

        # append path
        s = AntPath(path)
        cost = calculate_cost(s, dist_mat)
        s.cost = cost
        s.fitness = 1 / cost
        pop.append(s)

    return pop


def Ant_Colony_Algo(data, gen_num, size, alpha, beta, ro):
    # 1- generate distance matrix
    dist_mat = generate_distance_matrix(data)

    # 2- generate intial population
    pop = generat_population(data, size, dist_mat)

    # 3- generate intial population
    phormone_mat = initial_phromone_matrix(data, pop)

    for i in range(gen_num):
        # construct a new population of size the intial pop
        gen = construct_solution(data, dist_mat, phormone_mat, alpha, beta, size)
        # update the phromone matrix
        phormone_mat = update_phromone_matrix(phormone_mat, gen, ro)

    return gen

def plot_cities(cities):
    # Extract x and y coordinates into separate lists
    x_coords = [city.x for city in cities.path]
    y_coords = [city.y for city in cities.path]

    # Add the first city to the end to close the path
    x_coords.append(cities.path[0].x)
    y_coords.append(cities.path[0].y)

    # Create a Matplotlib figure
    fig, ax = plt.subplots()

    # Plot cities as scatter points
    ax.scatter(x_coords, y_coords)

    # Plot path between cities as lines
    for i in range(len(cities.path)):
        curr_city = cities.path[i]
        next_city = cities.path[(i+1)%len(cities.path)] # wrap around to the first city
        ax.plot([curr_city.x, next_city.x], [curr_city.y, next_city.y], marker='>')

    # Show the plot
    ax.set_title('Path by Ant-Colony')
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
            city_data[name] = city

    # Create a list of city instances from the dictionary values
    cities = list(city_data.values())

    # Set the Hyperpratmeters
    gen_num = 100
    size = 50
    ln = 15
    alpha = 1
    beta = 1
    ro = 0.3

    Solution= Ant_Colony_Algo(cities,gen_num,size,alpha,beta,ro)
    best = max(Solution, key=lambda x: x.fitness)
    total_cost = best.cost
    path = [city.name for city in best.path]

    print(f"The Total Cost is : {total_cost} ")
    print(f"THE Path is {path} ")
    plot_cities(best)