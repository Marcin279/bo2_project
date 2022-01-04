import src.data_structures as ds
import src.tabu_solution as tsol

import numpy as np


def test_solution_structures():
    # OK
    d = 1
    prod = np.random.randint(0, 2, 10)
    bilans = 456.1
    sol = ds.Solution(d, prod, bilans)
    print(sol)


def test_generate_initial_solution():
    terminarz = ds.return_calendar(3, 1, 2022, 15, 1, 2022)
    lista_produktow = ds.generuj_liste_produktow()
    # print(np.array(lista_produktow))
    lod1 = tsol.Lodowka(terminarz, lista_produktow)

    lod1.print_solution(lod1.generete_initial_solution())


def test_step1():
    terminarz = ds.return_calendar(3, 1, 2022, 15, 1, 2022)
    lista_produktow = ds.generuj_liste_produktow()
    # print(np.array(lista_produktow))
    lod1 = tsol.Lodowka(terminarz, lista_produktow)
    sol = lod1.generete_initial_solution()
    # lod1.print_solution(sol)

    sol = lod1.zwroc_liste_produktow(sol)
    print('type_sol', type(sol))
    print('\n\n')
    sol_step = lod1.step1(sol)
    print(sol_step)
    # lod1.print_solution(sol)


def test_check_capacity():
    terminarz = ds.return_calendar(3, 1, 2022, 15, 1, 2022)
    lista_produktow = ds.generuj_liste_produktow()
    # print(np.array(lista_produktow))
    lod1 = tsol.Lodowka(terminarz, lista_produktow)
    sol = lod1.generete_initial_solution()
    sol = lod1.zwroc_liste_produktow(sol)
    sol_step = lod1.step1(sol)
    ch_cap = lod1.check_capacity(sol_step)
    print(ch_cap)


def test_check_current_solution_in_tabu_list():
    terminarz1 = ds.return_calendar(3, 1, 2022, 15, 1, 2022)
    lista_produktow1 = ds.generuj_liste_produktow()
    lod1 = tsol.Lodowka(terminarz1, lista_produktow1)
    sol1 = lod1.generete_initial_solution()
    sol1 = lod1.zwroc_liste_produktow(sol1)
    sol_step1 = lod1.step1(sol1)
    sol_step1_1 = lod1.step1(sol_step1)
    lod1.tabu_list.append(sol_step1)
    lod1.tabu_list.append(sol_step1_1)
    print(np.array_equal(sol_step1, sol1))
    # print(sol1)
    print(lod1.tabu_list)
    check = lod1.check_current_sol_in_tabu_list(lod1.tabu_list, sol_step1)
    print(check)


def test_tabu_solution():
    terminarz = ds.return_calendar(1, 1, 2022, 30, 1, 2022)
    lista_produktow = ds.generuj_liste_produktow()
    lod1 = tsol.lodowka(terminarz, lista_produktow)
    lod1.tabu_solution()
    lod1.print_solution(lod1.best_solution)
    print(lod1.zwroc_najlepsze_rozwiazanie(lod1.best_solution))


if __name__ == '__main__':
    # print(ds.return_calendar(3, 1, 2022, 15, 1, 2022))
    # test_solution_structures()

    # test_generate_initial_solution()
    # test_step1()
    # test_check_capacity()
    # test_check_current_solution_in_tabu_list()
    test_tabu_solution()
