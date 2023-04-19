# Travelling-salesman-problem-using-some-Random-Search-Algorithms

![tsp](https://user-images.githubusercontent.com/125984328/233182623-8c761e15-6d1b-4edb-8dd2-393f2a06124b.jpg)
# Problem Defintion
The travelling salesman problem (TSP) is a problem that involves finding the shortest possible route that visits every city in a given list exactly once, before returning to the starting city. TSP has numerous practical applications, including in logistics, planning, and microchip production.
# Solution Techniques
I solved this problem using some heuristic and metaheuristic Algorithms (NN, GA & ACO)
## Nearest Neighbor Algorithm 
The nearest neighbour algorithm is easy to implement and executes quickly, but it can sometimes miss shorter routes which are easily noticed with human insight, due to its "greedy" nature.
Steps :
1. Initialize all vertices as unvisited.
2. Select an arbitrary vertex, set it as the current vertex u. Mark u as visited.
3. Find out the shortest edge connecting the current vertex u and an unvisited vertex v.
4. Set v as the current vertex u. Mark v as visited.
5. If all the vertices in the domain are visited, then terminate. Else, go to step 3.
## Genetics Algorithm
![image](https://user-images.githubusercontent.com/125984328/233184997-99210735-1648-400c-8972-421c406f9ff1.png)

Genetic Algorithm (GA) is a meta-heuristic algorithm that attempts to simulate natural selection to find the best path by crossing-over parents and producing fitter offspring.
Steps:.
1. Creating initial population.
2. Evaluation of each individual by fittness function.
3. Selecting the best genes.
4. Reproduction by Crossing over.
5. Mutating to introduce variations.
## Ant Colony Algorithm
![image](https://user-images.githubusercontent.com/125984328/233184709-424f7d97-6568-4459-9a1e-aec30de35892.png)

Ant Colony Optimization (ACO) Algorithm is a meta-heuristic algorithm where "ants" explore different paths leaving pheromones where they travel further leading the shorter distances to be crossed more and thus have more pheromones for others to follow.


These algorithms do not guarantee optimal solution, but rather reach a sub-optimal or near-optimal solution in a manageable time.
