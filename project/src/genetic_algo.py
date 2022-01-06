import numpy as np
import src.data_structures as ds
# from src.data_structures import
import copy
from typing import List, Union, Dict, Tuple, Set, Any
import random
from src.tabu_solution import lodowka

lista_produktow = np.array([
    [5.600e-01, 1.335e+03],
    [2.500e-01, 1.274e+03],
    [3.800e-01, 6.570e+02],
    [7.000e-02, 1.258e+03],
    [1.100e-01, 8.410e+02],
    [5.500e-01, 1.146e+03],
    [3.200e-01, 9.850e+02],
    [2.000e-02, 8.490e+02],
    [1.400e-01, 1.235e+03],
    [1.000e-01, 1.343e+03]])

ograniczenia = ds.Ograniczenia()


def print_solution2(data: List[List[int]], title: str = 'XD'):
    print(title, sep='\n')
    for i in range(len(data)):
        tmp = np.array(data[i])
        print(tmp)
        print('\n')


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


def eval_init_population(init_population):  # wyliczenie wartosci funkcji celu dla osobnika
    evaluated_init_population = []
    for i in range(len(init_population)):
        evaluated_init_population.append((init_population[i], evaluate_chromosome(init_population[i])))
    return evaluated_init_population


# Step 3. Choose P/2 parents from the current population via proportional selection.
def rulette(evaluated_init_population):
    """
    zwraca lista[decyzja, lista_prod, bilnas]
    :param evaluated_init_population:
    :return: lista[decyzja, lista_prod, bilnas]
    """


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
    for i in range(0, len(parents_list)-1):
        pairs_list.append((parents_list[i], parents_list[i + 1]))
    pairs_list.append((parents_list[-1], parents_list[0]))

    print('len(pairs_list)',len(pairs_list))
    return pairs_list


def crossover(pairs_list):
    offsprings_list = []
    for i in range(len(pairs_list)):
        # Step 6. Repeat Steps  4 and 5 until all parents are selected and mated.
        cutpoint = random.randint(1, len(pairs_list[i][0]) - 1)
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
def mutation_singular(macierz_pom_produktow, ile_zamian=None):
    macierz_pom_produktow2 = np.array(macierz_pom_produktow)


    if ile_zamian == None:
        ile_zamian = int(macierz_pom_produktow2.shape[0] / 7 * 30)


    for i in range(ile_zamian):
        kierunek_przesuniecia = [1, 2, 3, 4]  # 1 - gora, 2 - dol, 3-lewo, 4-
        x_idx = np.random.randint(0, macierz_pom_produktow2.shape[1])
        y_idx = np.random.randint(0, macierz_pom_produktow2.shape[0])
        if x_idx == 0:
            kierunek_przesuniecia.remove(4)
        elif x_idx == macierz_pom_produktow2.shape[1] - 1:
            kierunek_przesuniecia.remove(2)

        if y_idx == 0:
            kierunek_przesuniecia.remove(1)

        elif y_idx == macierz_pom_produktow2.shape[0] - 1:
            kierunek_przesuniecia.remove(3)

        kierunek_przesuniecia_wybor = random.choice(kierunek_przesuniecia)
        if kierunek_przesuniecia_wybor == 1:  # gora
            macierz_pom_produktow[y_idx][x_idx], macierz_pom_produktow[y_idx - 1][x_idx] = macierz_pom_produktow[
                                                                                               y_idx - 1][x_idx], \
                                                                                           macierz_pom_produktow[
                                                                                               y_idx][x_idx]
        elif kierunek_przesuniecia_wybor == 3:  # dol
            macierz_pom_produktow[y_idx][x_idx], macierz_pom_produktow[y_idx + 1][x_idx] = macierz_pom_produktow[
                                                                                               y_idx + 1][x_idx], \
                                                                                           macierz_pom_produktow[
                                                                                               y_idx][x_idx]

        elif kierunek_przesuniecia_wybor == 2:  # prawo
            macierz_pom_produktow[y_idx][x_idx], macierz_pom_produktow[y_idx][x_idx + 1] = macierz_pom_produktow[
                                                                                               y_idx][x_idx + 1], \
                                                                                           macierz_pom_produktow[
                                                                                               y_idx][x_idx]
        else:  # lewo
            macierz_pom_produktow[y_idx][x_idx], macierz_pom_produktow[y_idx][x_idx - 1] = macierz_pom_produktow[
                                                                                               y_idx][x_idx - 1], \
                                                                                           macierz_pom_produktow[
                                                                                               y_idx][x_idx]

    return macierz_pom_produktow


def mutation(offsprings_list, prob_od_mut=0.1, changes_no=None):
    offsprings_list_mutated = []
    for i in range(len(offsprings_list)):
        mutation = random.random()
        if mutation <= prob_od_mut:
            mutated = mutation_singular((offsprings_list[i]), changes_no)
            offsprings_list_mutated.append(mutated)
        else:
            offsprings_list_mutated.append((offsprings_list[i]))
    return offsprings_list_mutated


# !! napisac w dokumentacji o dostosowaniu plecaka do wag

# po mutacji mozemy  sprawdzac poprawnosc otrzymanego osobnika (czy spelnia zalozenia)
# jezeli nie to mozemy
# a) odrzucic go i do wynikowej listy osobnikow (nowej populacji) go nie wpisywac
#   -> zeby populacja sie nie zmniejszala mozemy ze starej populacji podmmieniac te osobniki o najgorszej wartosci f celu
# b) mozemy go probowac poprawiac (jezeli brakuje kalorii do dodawac produkty) -> zeby nie bylo problemu to mozemy zwiekszyc ktores z ograniczen
# z kotrego bysmy nie skorzystali rozwiazania trzeba bedzie dokladnie opisac w dokumenacji, bo to nie jest zbyt "standardowe" rozwiazanie

def check_offspring_singular(offspring):
    """
    jako parametr przyjmuje macierz w której wiersze reprezentują kolejne dni, natomiast
    kolumny listę produktów
    Zwraca bool - czy osobnik spelnia zalozenia, czy nie
    """
    # if offspring is None:
    #     offspring = np.empty((len(self.initial_solution), 10))
    #     for i in range(0, len(self.initial_solution)):
    #         offspring[i] = self.initial_solution[i][1]

    ponad_stan_lst_lodowka = []
    bilans_kalorie = []
    aktualny_stan_lodowki = ograniczenia.poczatkowy_stan_lodowki
    zawartosc_lodowki = []
    for row in range(len(offspring)):

        if not all([v == 0 for v in offspring[row]]):
            zawartosc_lodowki.append(offspring[row])
            aktualny_stan_lodowki += sum(offspring[row])
            ponad_stan_lst_lodowka.append(aktualny_stan_lodowki)

        aktualne_zuzycie = 0
        bilans_kalorie.append(0)
        while aktualne_zuzycie < ograniczenia.zapotrz_kal:
            if (len(np.nonzero(zawartosc_lodowki)[0])) > 0:
                id_row = np.nonzero(zawartosc_lodowki)[0][0]
                id_col = np.nonzero(zawartosc_lodowki)[1][0]
                jedzony_produkt = lista_produktow[id_col]

                zawartosc_lodowki[id_row][id_col] = 0
                kalorycznosc = jedzony_produkt[1]
                aktualne_zuzycie += kalorycznosc
                aktualny_stan_lodowki -= 1

            else:
                bilans_kalorie.append(aktualne_zuzycie - ograniczenia.zapotrz_kal)
                break
    if all([elem <= ograniczenia.maksymalna_poj_lodowki for elem in
            ponad_stan_lst_lodowka]) and all([elem == 0 for elem in bilans_kalorie]):
        return 1
    return 0


def check_offspring(offsprings_list_mutated):
    offsprings_checked = []
    for i in range(len(offsprings_list_mutated)):
        offs_copy = copy.deepcopy(offsprings_list_mutated[i])
        offspring_ok = check_offspring_singular(offs_copy)

        if offspring_ok:
            offsprings_checked.append(offsprings_list_mutated[i])
        else:
            continue
    return offsprings_checked


# Step 7. Replace old population of chromosomes with new one.

def if_row_has_zero(row: List[int]) -> int:
    if any(row):
        return 1  
    else:
        return 0


def evaluate_1(individual: List[List[int]]):
    sum = 0
    for elem in individual:
        sum += if_row_has_zero(elem)
    return sum


# Step 8. Evaluate the fitness of each chromosome in the new population.
def replace_old_pop_with_new_one(old_population: List[List[List[int]]], new_population: List[List[List[int]]]):
    print('len(old_population)',len(old_population))
    print('len(new_population)',len(new_population))


    result_for_old = []
    for elem in old_population:
        pair = elem, evaluate_1(elem)
        result_for_old.append(pair)
    result_for_old = sorted(result_for_old, key=lambda t: t[1], reverse=False)
    print('len(result_for_old) po sortowaniu',len(result_for_old))


    result_for_new = []
    for elem in new_population:
        pair = elem, evaluate_1(elem)
        result_for_new.append(pair)
    print('len(result_for_new) po eval',len(result_for_new))


    for _ in range(0, len(new_population)):
        if len(result_for_old)!=0:
            tmp = result_for_old.pop()
        else:
            break
    print('len(result_for_old) po usuwaniu',len(result_for_old))


    for i in range(0, len(result_for_new)):
        result_for_old.append(result_for_new[i])
    print('len(result_for_old) po dodawaniu',len(result_for_old))


    result_for_old = sorted(result_for_old, key=lambda t: t[1], reverse=False)
    print('len(result_for_old) do zwrocenia',len(result_for_old))

    return result_for_old

def pull_parents_form_parents_longer(old_population):
    parents = []
    for i in range(len(old_population)):
        parents.append([])
        for j in range(len(old_population[i])):
            parents[i].append(old_population[i][j][1])
    return parents


# Step 9. Terminate if the number of generations meets some upper bound; otherwise go to Step3.

def change_new_popul_to_other_format(new_population):
    formatted = []

    for elem in (new_population):
        list = []
        for j in range(len(elem[0])):
            decision = if_row_has_zero(elem[0][j])
            list.append([decision, elem[0][j], 0])
        formatted.append(list)

    return formatted


def genetic_algo(upper_bound, lista_produktow, terminarz, len_init_population, probability = 0.1, liczba_zamian = None):


    #osobniki poczatkowe
    init_specimen = init_population(len_init_population, terminarz, lista_produktow)

    i = 0
    while i< upper_bound:
        #osobniki poczatkowe plus wartosc f celu
        init_specimen_f_celu = eval_init_population(init_specimen)

        # zwraca połowę poczatkowych osobnikow przez losowanie
        # prawdopodobienstwo wybrania osobnika do krzyzowania jest odwrotnie proporcjonalne do wartosci funkcji celu
        # (minimalizujemy jej wartosc)
        rull = rulette(init_specimen_f_celu)

        # łaczenie wybranych w losowaniu osobników w pary
        pairs = return_pairs(rull)

        # krzyżowanie rodziców - nowa populacja
        offspring = crossover(pairs)

        # mutowanie osobników z prawdopodobienstwem wystapienia mutacji = probability (wartosc domyslna  = 0.1)
        # oraz liczba zamian przy niej wykonywanych = liczba_zamian (wartosc domysna ~= 30 zamian na tydzień)
        offs_mut = mutation(offspring, prob_od_mut=probability, changes_no = liczba_zamian)

        # sprawdzenie poprawności otrzymanych po krzyzowaniu i mutacji osobników (bilans kaloryczny oraz upper bound lodowki)
        offspings_checked = check_offspring(offs_mut)

        # zastąpienie osobnikow z poprzedniej populacji o najgorszych wartosciach funkcji celu przez nowe osobniki
        x = replace_old_pop_with_new_one(pull_parents_form_parents_longer(rull), offspings_checked)
        init_specimen  = change_new_popul_to_other_format(x)

        i+=1

    return x