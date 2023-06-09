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

class Chromosome:
    def __init__(self, path):
        self.path = path
        self.fitness = -1
        self.cost = -1

    def __repr__(self):
        return f'<Tour:\tfitness: {self.fitness},\tPath:\n{self.path}>'


def calculate_distance(city1, city2):
    return np.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)

def calculate_cost(chromosome, distance_matrix):
    total_cost = 0
    path = chromosome.path
    n = len(path)
    # Calculate the cost of traversing the path in the chromosome.
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

def fitness_score(population):
    scores = []
    # Calculate the cost for each chromosome in the population.
    for chromosome in population:
        cost = calculate_cost(chromosome)
        scores.append(cost)
    scores = np.array(scores)
    # Sort the chromosomes by ascending cost.
    sorted_indices = np.argsort(scores)
    sorted_chromosomes = [population[i] for i in sorted_indices]
    sorted_scores = list(scores[sorted_indices])
    return sorted_scores, sorted_chromosomes

def selection(population, k):
    candidates = random.choices(population, k=k)
    return max(candidates, key=lambda x: x.fitness)

def elitism(percent, old_pop):
    n = int(percent*len(old_pop))
    sort = sorted(old_pop, key = lambda x: x.fitness, reverse=True)
    return sort[:n+1]


def partial_crossover(parent1, parent2, distance_matrix):

    # Step 1: Split the path of each parent into three ranges.
    split_range1 = random.randint(1, len(parent1.path) - 2)
    split_range2 = random.randint(1, len(parent1.path) - 2)

    # Swap split_range1 and split_range2 if split_range1 > split_range2.
    if split_range1 > split_range2:
        split_range1, split_range2 = split_range2, split_range1

    # Step 2: Create two child chromosomes as copies of the parent chromosomes.
    child1 = deepcopy(parent1)
    child2 = deepcopy(parent2)

    # Step 3: Iterate over the range between split_range1 and split_range2, and perform crossover.
    for i in range(split_range1, split_range2 + 1):
        # Check if the city at index i in child1 also appears in parent2 between split_range1 and split_range2.
        if child1.path[i] in [parent2.path[j] for j in range(split_range1, split_range2 + 1)]:
            # Find the index of the city in parent2.
            index = parent2.path.index(child1.path[i])
            # Swap the cities at index i and index in child1.
            child1.path[i], child1.path[index] = child1.path[index], child1.path[i]

        # Check if the city at index i in child2 also appears in parent1 between split_range1 and split_range2.
        if child2.path[i] in [parent1.path[j] for j in range(split_range1, split_range2 + 1)]:
            # Find the index of the city in parent1.
            index = parent1.path.index(child2.path[i])
            # Swap the cities at index i and index in child2.
            child2.path[i], child2.path[index] = child2.path[index], child2.path[i]

    # Step 4: Calculate the cost and fitness of each child chromosome.
    child1.cost = calculate_cost(child1, distance_matrix)
    child1.fitness = 1 / child1.cost
    child2.cost = calculate_cost(child2, distance_matrix)
    child2.fitness = 1 / child2.cost

    # Step 5: Return the two new child chromosomes as a tuple.
    return child1, child2

def crossover(probability, population, dist_mat):
    # Choose the two fittest candidates using K-Tournament Selection
    parent1 = selection(population, 5)
    parent2 = selection(population, 5)

    # If either parent is None, return the other parent as both children
    if not parent1:
        return parent2, parent2
    elif not parent2:
        return parent1, parent1

    # Apply crossover with probability 'probability'
    if random.random() <= probability:
        child1, child2 = partial_crossover(parent1, parent2, dist_mat)
    else:
        child1, child2 = parent1, parent2

    # Evaluate fitness of children
    child1.cost = calculate_cost(child1, dist_mat)
    child1.fitness = 1 / child1.cost
    child2.cost = calculate_cost(child2, dist_mat)
    child2.fitness = 1 / child2.cost

    # Return fittest children as new parents
    if child1.fitness > parent1.fitness:
        parent1 = child1
    if child2.fitness > parent2.fitness:
        parent2 = child2

    return parent1, parent2


def mutation(prob, pop, dist_mat):
    new_pop = []

    # apply mutation on each chrom in the population
    for chrom in pop:
        c = deepcopy(chrom)

        # apply mutation with probability prob
        if random.random() < prob:
            # choose two random indices
            i, j = sorted(random.sample(range(len(c.path)), 2))

            # reverse the order of the subpath between the chosen indices
            c.path[i:j + 1] = reversed(c.path[i:j + 1])

        # calc the cost for the mutated crom
        cost = calculate_cost(c, dist_mat)
        c.cost = cost
        c.fitness = 1 / cost

        # add it to the new pop
        new_pop.append(c)

    return new_pop

def generat_population(lst_cities, pop_size, dist_mat):
    population = []

    # create random chromosomes
    for i in range(pop_size):
        path = lst_cities.copy()
        random.shuffle(path)

        chrom = Chromosome(path)

        # calculate the cost for the created chrom path
        cost = calculate_cost(chrom, dist_mat)
        chrom.cost = cost
        chrom.fitness = 1 / cost

        # add the chrom to the population
        population.append(chrom)

    return population


def genetic_algo(data, size=50, cross_over_rate=0.6, mutation_rate=0.1, elitism_per=0.1, gen_num=100):
    best_chromo = []
    best_score = []
    # 1- generate distance matrix
    dist_mat = generate_distance_matrix(data)

    # 2- generate intial population
    population = generat_population(data, size, dist_mat)

    n = len(population)
    for i in range(gen_num):
        new_pop = []
        # add elitism to the new pop

        new_pop = elitism(elitism_per, population)
        while (len(new_pop) < n):
            # apply crossover until new pop size reach the old pop size
            new_child1, new_child2 = crossover(cross_over_rate, population, dist_mat)
            new_pop.append(new_child1)
            new_pop.append(new_child2)

        if len(new_pop) != n:
            new_pop.pop()

        # apply mutation on the new pop
        new_pop = mutation(mutation_rate, new_pop, dist_mat)

        # update pop
        population = new_pop

    return population


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
    ax.set_title('Path by Genetic-Algo')
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
    size = 50
    cross_over_rate = 0.6
    mutation_rate = 0.1
    elitism_per = 0.02
    gen_num = 100

    generation = genetic_algo(cities, size, cross_over_rate, mutation_rate, elitism_per, gen_num)
    best = max(generation, key=lambda x: x.fitness)
    total_cost = best.cost
    path = [city.name for city in best.path]

    print(f"The Total Cost is : {total_cost} ")
    print(f"THE Path is {path} ")
    plot_cities(best)