import src.data_structures as ds
import src.tabu_solution as tsol
import src.genetic_algo as gen

import numpy as np

lista_produktow1 = np.array([[5.600e-01, 1.335e+03],
                             [2.500e-01, 1.274e+03],
                             [3.800e-01, 6.570e+02],
                             [7.000e-02, 1.258e+03],
                             [1.100e-01, 8.410e+02],
                             [5.500e-01, 1.146e+03],
                             [3.200e-01, 9.850e+02],
                             [2.000e-02, 8.490e+02],
                             [1.400e-01, 1.235e+03],
                             [1.000e-01, 1.343e+03]])

lista_produktow2 = np.array([[6.000e-02, 9.300e+02],
                             [4.000e-01, 8.160e+02],
                             [3.000e-01, 1.242e+03],
                             [5.000e-01, 1.498e+03],
                             [6.400e-01, 8.930e+02],
                             [2.800e-01, 1.134e+03],
                             [1.700e-01, 6.590e+02],
                             [6.100e-01, 1.315e+03],
                             [1.800e-01, 3.330e+02],
                             [2.100e-01, 8.580e+02]])

lista_produktow3 = np.array([[4.900e-01, 6.580e+02],
                             [4.400e-01, 8.960e+02],
                             [1.000e-01, 8.500e+02],
                             [2.200e-01, 1.145e+03],
                             [2.700e-01, 5.880e+02],
                             [1.700e-01, 8.650e+02],
                             [6.000e-02, 7.740e+02],
                             [1.500e-01, 9.500e+02],
                             [4.500e-01, 6.980e+02],
                             [2.200e-01, 9.710e+02]])

lista_produktow = lista_produktow3

calendar = ds.return_calendar(3, 1, 2022, 25, 1, 2022)


class Data:
    lista_produktow = lista_produktow
    kalendarz = calendar


class ParamsToGeneticAlgo:
    iteration = 1000
    prawdopobienstwo_mutacji = 0.9
    ilosc_osobnikow_do_reprodukcji = 20


class ParamsToTabuSearch:
    ograniczenia = ds.Ograniczenia
    # ograniczenia.zapotrz_kal = 3000
    ograniczenia.kryterium_stopu = 1000


def genetic_algo_print(iteracje, lista_produktow, calendar, ilosc_osobnikow_pierw, prawdopodobienstwo_wyst_mutacji):
    print("======= Algorytm genetyczny =======\n\n")
    print(lista_produktow)
    print(f'kryterium stopu, iteracje = {iteracje}')
    solution = gen.genetic_algo(iteracje, lista_produktow, calendar, ilosc_osobnikow_pierw,
                                prawdopodobienstwo_wyst_mutacji)


def tabu_search_print(data: Data, params: ParamsToTabuSearch):
    print("======= TABU SEARCH =======\n\n")
    print(data.lista_produktow)
    it = params.ograniczenia.kryterium_stopu
    print("Dla iteracji: ", it)
    terminarz = data.kalendarz
    lista_produktow = data.lista_produktow
    lod1 = tsol.lodowka(terminarz, lista_produktow)
    lod1.kryterium_stopu = it
    lod1.tabu_solution()
    lod1.print_solution(lod1.best_solution)


if __name__ == '__main__':

    params_to_genetic_algo = ParamsToGeneticAlgo
    data = Data

    params_to_tabu_search = ParamsToTabuSearch

    # Tu wybierz którą metodę chcesz liczyć
    # True = algorytm genetyczny
    # False = Tabu Search
    wybierz_metode_genetic_algo: bool = False

    if wybierz_metode_genetic_algo is True:
        genetic_algo_print(iteracje=params_to_genetic_algo.iteration, lista_produktow=data.lista_produktow,
                           calendar=data.kalendarz,
                           ilosc_osobnikow_pierw=params_to_genetic_algo.ilosc_osobnikow_do_reprodukcji,
                           prawdopodobienstwo_wyst_mutacji=params_to_genetic_algo.prawdopobienstwo_mutacji)
    else:
        tabu_search_print(data, params_to_tabu_search)
