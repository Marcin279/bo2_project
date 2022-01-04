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


def eval_init_population(init_population): #wyliczenie wartosci funkcji celu dla osobnika
    evaluated_init_population = []
    for i in range(len(init_population)):
        evaluated_init_population.append((init_population[i], evaluate_chromosome(init_population[i])))
    return evaluated_init_population


# Step 3. Choose P/2 parents from the current population via proportional selection.
def rulette(evaluated_init_population):
    #zwraca lista[decyzja, lista_prod, bilnas]

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
        parents_list.append(list_eval.pop(chosen_point)[0])

    return parents_list


# Step 4. Randomly select two parents to create offspring using crossover operator.
def return_pairs(parents_list):
    pairs_list = []
    for i in range(0, len(parents_list), 2):
        pairs_list.append((parents_list[i], parents_list[i+1]))
    return pairs_list

def crossover(pairs_list):
    offsprings_list = []
    for i in range(len(pairs_list)):
    # Step 6. Repeat Steps  4 and 5 until all parents are selected and mated.
        cutpoint = random.randint(1, len(pairs_list[i][0])-1)
        print('cutpoint = ',cutpoint)
        offspring1 = []
        offspring2 = []
        for j in range(len(pairs_list[i][0])):
            if j < cutpoint:
                offspring1.append(pairs_list[i][0][j][1])
                offspring2.append(pairs_list[i][1][j][1])
            else:
                offspring1.append(pairs_list[i][1][j][1])
                offspring2.append(pairs_list[i][0][j][1])
        offsprings_list.append(offspring1)
        offsprings_list.append(offspring2)
    return offsprings_list
                            
# Step 5. Apply mutation operators for minor changes in the results.
def mutation_singular(self, macierz_pom_produktow, ile_zamian):
    if ile_zamian == None:
        ile_zamian = int(macierz_pom_produktow.shape[0]/7*30)
    
    for i in range(ile_zamian):
        kierunek_przesuniecia = [1, 2, 3, 4]  # 1 - gora, 2 - dol, 3-lewo, 4-
        x_idx = np.random.randint(0, macierz_pom_produktow.shape[1])
        y_idx = np.random.randint(0, macierz_pom_produktow.shape[0])
        if x_idx == 0:
            kierunek_przesuniecia.remove(4)
        elif x_idx == macierz_pom_produktow.shape[1] - 1:
            kierunek_przesuniecia.remove(2)

        if y_idx == 0:
            kierunek_przesuniecia.remove(1)

        elif y_idx == macierz_pom_produktow.shape[0] - 1:
            kierunek_przesuniecia.remove(3)

        kierunek_przesuniecia_wybor = random.choice(kierunek_przesuniecia)
        if kierunek_przesuniecia_wybor == 1:  # gora
            macierz_pom_produktow[y_idx, x_idx], macierz_pom_produktow[y_idx - 1, x_idx] = macierz_pom_produktow[
                                                                                                y_idx - 1, x_idx], \
                                                                                            macierz_pom_produktow[
                                                                                                y_idx, x_idx]
        elif kierunek_przesuniecia_wybor == 3:  # dol
            macierz_pom_produktow[y_idx, x_idx], macierz_pom_produktow[y_idx + 1, x_idx] = macierz_pom_produktow[
                                                                                                y_idx + 1, x_idx], \
                                                                                            macierz_pom_produktow[
                                                                                                y_idx, x_idx]

        elif kierunek_przesuniecia_wybor == 2:  # prawo
            macierz_pom_produktow[y_idx, x_idx], macierz_pom_produktow[y_idx, x_idx + 1] = macierz_pom_produktow[
                                                                                                y_idx, x_idx + 1], \
                                                                                            macierz_pom_produktow[
                                                                                                y_idx, x_idx]
        else:  # lewo
            macierz_pom_produktow[y_idx, x_idx], macierz_pom_produktow[y_idx, x_idx - 1] = macierz_pom_produktow[
                                                                                                y_idx, x_idx - 1], \
                                                                                            macierz_pom_produktow[
                                                                                                y_idx, x_idx]

    return macierz_pom_produktow


def mutation(offsprings_list, prob_od_mut = 0.1, changes_no = None):
    offsprings_list_mutated = []
    for i in range(len(offsprings_list)):
        mutation = random.random()
        if mutation <= prob_od_mut:
            offsprings_list_mutated.append(mutation_singular(offsprings_list[i]))
        else:
            offsprings_list_mutated.append(offsprings_list[i])
    return offsprings_list_mutated

# Step 7. Replace old population of chromosomes with new one.

# Step 8. Evaluate the fitness of each chromosome in the new population.

# Step 9. Terminate if the number of generations meets some upper bound; otherwise go to Step  3.
