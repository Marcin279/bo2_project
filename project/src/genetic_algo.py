import numpy as np
import src.data_structures as ds
# from src.data_structures import
import copy
from typing import List, Union, Dict, Tuple, Set, Any
import random
from src.tabu_solution import lodowka


def print_solution(solution):
    S = ''
    for elem in solution:
        S += f"d: {elem[0]}  lst: {elem[1]}  b: {elem[2]}\n"
    print(S)


# Step 1. Create an initial population of P chromosomes.
def init_population(n, terminarz, lista_produktow):
    """
    Parameters:
    n - ilość osobników do otrzymania
    terminarz - lista dni na jakie chcemy zrobić rozpiskę
    lista_produktow - stała lista produktów z ich wagą i kalorycznością

    Returns:
    init_population (list): lista rozwiązań początkowych
    """
    init_population = []
    for i in range(n):
        lodowka_ = lodowka(terminarz, lista_produktow).initial_solution
        init_population.append(lodowka_)
    return init_population


# Step 2. Evaluate the fitness of each chromosome.
def evaluate_chromosome(solution):
    min = 0
    for i in range(len(solution)):
        min += solution[i][0]
    return min


def eval_init_population(init_population):
    evaluated_init_population = []
    for i in range(len(init_population)):
        evaluated_init_population.append((init_population[i], evaluate_chromosome(init_population[i])))
    return evaluated_init_population


# Step 3. Choose P/2 parents from the current population via proportional selection.
def rulette(evaluated_init_population):
    parents_list = []
    iter = 0
    list_eval = copy.deepcopy(evaluated_init_population)

    how_many = len(evaluated_init_population) // 2
    if how_many % 2 != 0:
        how_many += 1

    while iter < how_many:
        iter += 1
        suma_po_wyjsciach = 0
        for i in range(len(list_eval)):
            suma_po_wyjsciach += list_eval[i][1]

        stop_points = [0]
        for j in range(len(list_eval)):
            stop_points.append(1 / list_eval[j][1])
        sum_stop_points = sum(stop_points)
        normalized_stop_points = [point / sum_stop_points for point in stop_points]
        normalized_stop_points_summed = [normalized_stop_points[0]]
        for i in range(1, len(normalized_stop_points)):
            normalized_stop_points_summed.append(normalized_stop_points_summed[i - 1] + normalized_stop_points[i])

        rand = random.random()
        chosen_point = 0  # indeks rodzica
        for i in range(len(normalized_stop_points_summed) - 1):
            if normalized_stop_points_summed[i] <= rand < normalized_stop_points_summed[i + 1]:
                chosen_point = i
                break
            else:
                continue
        parents_list.append(list_eval.pop(chosen_point))

    return parents_list


# Step 4. Randomly select two parents to create offspring using crossover operator.
def return_pairs():
    pass

# Step 5. Apply mutation operators for minor changes in the results.

# Step 6. Repeat Steps  4 and 5 until all parents are selected and mated.

# Step 7. Replace old population of chromosomes with new one.

# Step 8. Evaluate the fitness of each chromosome in the new population.

# Step 9. Terminate if the number of generations meets some upper bound; otherwise go to Step  3.
