import numpy as np
import src.data_structures as ds
import copy
from typing import List, Union, Dict, Tuple, Set, Any
import random
from src.tabu_solution import lodowka


najlepsze_rozwiazanie = 100

ograniczenia = ds.Ograniczenia()


def print_solution2(data: List[List[int]], title: str = '...'):
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


# inicjalizacja populacji p osobników
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


# wyliczenie wartości funkcji celu osobnika
def evaluate_chromosome(solution):
    """
    Parameters:
    solution - osobnik
    Returns:
    fitness: wartość funkcji celu dla danego osobnika
    """
    fitness = 0
    for i in range(len(solution)):
        fitness += solution[i][0]
    return fitness


# wyliczenie wartosci funkcji celu dla populacji
def eval_init_population(init_population):
    evaluated_init_population = []
    for i in range(len(init_population)):
        evaluated_init_population.append((init_population[i], evaluate_chromosome(init_population[i])))
    return evaluated_init_population


# wybranie osobnikow do krzyżowania - wybierane jest n najlepszych
# ponieważ po krzyzowaniu niektóre osobniki potomne nie spełniają ograniczeń
# i nie sa dalej przekazywane, n jest stałą liczbą równą połowie długości początkowej populacji
def choose_parents(evaluated_init_population, len_init_population):
    """
    Parameters:
    evaluated_init_population - lista osobników wraz z ich wartościami funkcji celu
    len_init_population - długość początkowej populacji
    Returns:
    parents_list - lista rodziców wybranych do krzyżowania
    """

    parents_list = []
    ite = 0
    list_eval = copy.deepcopy(evaluated_init_population)

    how_many = len_init_population // 2
    if how_many % 2 != 0:
        how_many += 1

    lista_pomocnicza2 = []
    while ite < how_many:
        ite += 1
        elem = list_eval.pop(0)
        parents_list.append(elem[0])
        lista_pomocnicza2.append(elem[1])

    return parents_list


# podział rodziców w pary: 1-2, 3-4 etc
def return_pairs(parents_list):
    pairs_list = []
    for i in range(0, len(parents_list) - 1, 2):
        pairs_list.append((parents_list[i], parents_list[i + 1]))
    return pairs_list


# crossover
def crossover(pairs_list):
    offsprings_list = []
    for i in range(len(pairs_list)):
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


# mutacja pojedynczego osobnika
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


# mutowanie osobników
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


# sprawdzenie poprawności jednego osobnika

def check_offspring_singular(offspring, lista_produktow):
    """
    jako parametr przyjmuje macierz w której wiersze reprezentują kolejne dni, natomiast
    kolumny listę produktów
    Zwraca bool - czy osobnik spelnia zalozenia, czy nie
    """

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


# sprawdzenie poprawności pojedynczego osobnika po krzyżowaniu i mutacji

def check_offspring(offsprings_list_mutated, lista_produktow):
    offsprings_checked = []
    for i in range(len(offsprings_list_mutated)):
        offs_copy = copy.deepcopy(offsprings_list_mutated[i])
        offspring_ok = check_offspring_singular(offs_copy, lista_produktow)

        if offspring_ok:
            offsprings_checked.append(offsprings_list_mutated[i])
        else:
            continue
    return offsprings_checked


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


# sprawdzenie poprawności osobników po krzyżowaniu i mutacji
def replace_old_pop_with_new_one(old_population: List[List[List[int]]], new_population: List[List[List[int]]]):
    result_for_old = []
    for elem in old_population:
        pair = elem, evaluate_1(elem)
        result_for_old.append(pair)

    result_for_new = []
    for elem in new_population:
        pair = elem, evaluate_1(elem)
        result_for_new.append(pair)

    nowa_lista = []
    for i in range(0, len(result_for_new)):
        nowa_lista.append(result_for_new[i])
    for i in range(0, len(result_for_old)):
        nowa_lista.append(result_for_old[i])

    nowa_lista = sorted(nowa_lista, key=lambda t: t[1], reverse=False)

    return nowa_lista


# podmiana formatu rodziców
def pull_parents_form_parents_longer(old_population):
    parents = []
    for i in range(len(old_population)):
        parents.append([])
        for j in range(len(old_population[i])):
            parents[i].append(old_population[i][j][1])
    return parents


def change_new_popul_to_other_format(new_population):
    formatted = []

    for elem in (new_population):
        list = []
        for j in range(len(elem[0])):
            decision = if_row_has_zero(elem[0][j])
            list.append([decision, elem[0][j], 0])
        formatted.append(list)

    return formatted


def genetic_algo(upper_bound, lista_produktow, terminarz, len_init_population, probability=0.1, liczba_zamian=None):
    global najlepsze_rozwiazanie
    # osobniki poczatkowe
    init_specimen = init_population(len_init_population, terminarz, lista_produktow)

    i = 0
    while i < upper_bound:
        # osobniki poczatkowe plus wartosc f celu
        init_specimen_f_celu = eval_init_population(init_specimen)

        # zwraca polowe dlugosci pierwotnej listy osobników najlepszych osobników
        parents = choose_parents(init_specimen_f_celu, len_init_population)
        copy_parents = copy.deepcopy(parents)

        # łaczenie wybranych w losowaniu osobników w pary
        pairs = return_pairs(parents)

        # krzyżowanie rodziców - nowa populacja
        offspring = crossover(pairs)

        # mutowanie osobników z prawdopodobienstwem wystapienia mutacji = probability (wartosc domyslna  = 0.1)
        # oraz liczba zamian przy niej wykonywanych = liczba_zamian (wartosc domysna ~= 30 zamian na tydzień)
        offs_mut = mutation(offspring, prob_od_mut=probability, changes_no=liczba_zamian)

        # sprawdzenie poprawności otrzymanych po krzyzowaniu i mutacji osobników (bilans kaloryczny oraz upper bound lodowki)
        offspings_checked = check_offspring(offs_mut, lista_produktow)

        # dodanie do starych osobnikow, nowo powstalych
        x = replace_old_pop_with_new_one(pull_parents_form_parents_longer(copy_parents), offspings_checked)

        if x[0][1] < najlepsze_rozwiazanie:
            print('iteracja = ', i, 'f.celu = ', x[0][1])
            najlepsze_rozwiazanie = x[0][1]

        # len(x) jest miedzy [len(rodzice), 2*len(rodzice)]
        init_specimen = change_new_popul_to_other_format(x)
        i += 1

    return x

    ####### ŚMIECI ############
# pierwotna wersja wyboru osobników do krzyżowania
# została odrzucona, ponieważ różnice między f.celu dla lepszych osobników były niewielkie,
# co przekłądało się na to że z dużym pradopodobieństwem nie były one przekazywane do dalszej populacji
# def rulette_pierwotne(evaluated_init_population):
#     """
#     Parameters:
#     evaluated_init_population - lista osobników wraz z ich wartościami funkcji celu
#     Returns:
#     parents_list - lista rodziców wybranych do krzyżowania
#     """

#     parents_list = []
#     ite = 0
#     list_eval = copy.deepcopy(evaluated_init_population)

#     how_many = len(evaluated_init_population) // 2
#     if how_many % 2 != 0:
#         how_many += 1

#     while ite < how_many:
#         ite += 1
#         suma_po_wyjsciach = 0
#         for i in range(len(list_eval)):
#             suma_po_wyjsciach += list_eval[i][1]

#         stop_points = [0]
#         for j in range(len(list_eval)):
#             stop_points.append(1 / list_eval[j][1])
#         sum_stop_points = sum(stop_points)
#         normalized_stop_points = [point / sum_stop_points for point in stop_points]
#         normalized_stop_points_summed = [normalized_stop_points[0]]
#         for i in range(1, len(normalized_stop_points)):
#             normalized_stop_points_summed.append(normalized_stop_points_summed[i - 1] + normalized_stop_points[i])

#         rand = random.random()
#         chosen_point = 0  # indeks rodzica
#         for i in range(len(normalized_stop_points_summed) - 1):
#             if normalized_stop_points_summed[i] <= rand < normalized_stop_points_summed[i + 1]:
#                 chosen_point = i
#                 break
#             else:
#                 continue
#         parents_list.append(list_eval.pop(chosen_point)[0])

#     return parents_list


# #inne przydzielanie rodziców w pary - losowe (dawało gorsze wyniki)
# def return_pairs(parents_list):
#     pairs_list = []
#     # for i in range(0, len(parents_list)-1, 2):
#     #     pairs_list.append((parents_list[i], parents_list[i + 1]))

#     parents_list_copy = copy.deepcopy(parents_list)
#     random.shuffle(parents_list_copy)
#     while parents_list_copy:
#         elem1 = parents_list_copy.pop(0)
#         elem2 = parents_list_copy.pop(0)
#         pairs_list.append((elem1, elem2))
#     return pairs_list
