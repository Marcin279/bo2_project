import numpy as np
import src.data_structures as ds
# from src.data_structures import
import copy
from typing import List, Union, Dict, Tuple, Set, Any
import random


class Lodowka:
    ograniczenia = ds.Ograniczenia
    poczatkowy_stan_lodowki = ograniczenia.poczatkowy_stan_lodowki  # poczatkowy stan lodowki

    maksymalna_poj_lodowki = ograniczenia.maksymalna_poj_lodowki  # maksymalna ilosc produktow w lodowce
    maks_liczba = ograniczenia.maks_liczba  # maksymalna ilosc tego samego produktu
    N = ograniczenia.N  # tbd
    max_poj_plecaka = ograniczenia.max_poj_plecaka  # kg maksymalna pojemnosc_plecaka
    zapotrz_kal = ograniczenia.zapotrz_kal  # Zapotrzebowanie kaloryczne w danym dniu - w każdym dniu tyle samo
    kryterium_stopu = ograniczenia.kryterium_stopu  # maksymalna ilosc iteracji

    def __init__(self, terminarz, lista_produktow):
        """
        parameters:
        terminarz - Przechowuje informacje w postaci (data, dzien_tygodnia, maksymalna_dopuszczalna_waga)
        jeżeli maksymalna_dopuszczalna_waga = 0 wtedy w danym dniu nie idziemy do sklepu w przeciwnym wypadku jest równe max_poj_plecaka

        lista produktow - przechowuje informacja w postaci np.ndarray, gdzie pierwsze

        initial_solution przyjmuje to co zwraca metoda generate_initial_solution()
        """
        self.terminarz = terminarz
        self.lista_produktow = lista_produktow
        self.initial_solution = self.generete_initial_solution()
        # self.aktualny_stan_lodowki = x0
        # self.aktualne_zapotrzebowanie_kaloryczne = zapotrz_kal
        self.tabu_list = []  # Lista tabu
        self.best_solution = self.initial_solution

    def generete_initial_solution(self) -> List[Union[ds.Solution, Any]]:
        """
        Returns:
        init_solution (list): Rozwiązanie początkowe, baza do kolejnych kroków.
        Kolejne elementy init_solution oznaczają kolejne dni terminarza.
        Przykładowe elementy listy:
        [1, [0, 0, 1, 0, 0, 1, 0, 1, 1, 1], 0]
        [0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], -19.0]
        gdzie:  init_solution[i][0]: decyzja o pójściu na zakupy
                init_solution[i][1]: lista wziętych produktów
                init_solution[i][2]: bilans kalorii

        """
        init_solution = []  # Rozwiązanie początkowe
        self.lista_produktow = np.array(self.lista_produktow)
        aktualny_stan_lodowki = self.poczatkowy_stan_lodowki
        zawartosc_lodowki = []
        for i in range(len(self.terminarz)):
            aktualny_stan_plecaka = 0
            if self.terminarz[i][2] != 0:
                teoretyczna_lista_zakupow = random.sample(range(10), 10)
                # print('ttt\n', teoretyczna_lista_zakupow)
                lista_1 = [0] * len(self.lista_produktow)
                count = 0
                while True and count < len(self.lista_produktow):
                    indeks_produktu_ktory_bierzemy = teoretyczna_lista_zakupow[count]
                    waga_produktu = self.lista_produktow[indeks_produktu_ktory_bierzemy][0]
                    # print('idx\n', indeks_produktu_ktory_bierzemy)
                    # sprawdzenie czy produkt który zamierzamy wziąć spełnia ograniczenia lodówki i plecaka:
                    if aktualny_stan_lodowki + 1 <= self.maksymalna_poj_lodowki and aktualny_stan_plecaka + waga_produktu <= self.max_poj_plecaka:
                        lista_1[indeks_produktu_ktory_bierzemy] = 1
                        aktualny_stan_lodowki += 1
                        aktualny_stan_plecaka += waga_produktu
                        count += 1
                    else:
                        break
                solution = ds.Solution(decyzja=1, lista_produktow=lista_1, bilans=0)
                init_solution.append(solution)
                zawartosc_lodowki.append(lista_1)
                # print('sol1\t', solution)

            elif self.terminarz[i][2] == 0:
                temp = [0 for i in range(len(self.lista_produktow))]
                # print(self.lista_produktow)
                print('x')
                # print('tmp\t')
                solution = ds.Solution(0, temp, 0)
                init_solution.append(solution)
                # print('sol2\t', solution)

            wiersz_copy = copy.deepcopy(init_solution[-1])
            # aktualizacja zużycia produktow (sprawdzenie w których dniach będzie niedobór kaloryczny (poprawiane następnie w check_kalorie())):
            aktualne_zuzycie = 0
            while aktualne_zuzycie < self.zapotrz_kal:
                if (len(np.nonzero(zawartosc_lodowki)[0])) > 0:
                    id_row = np.nonzero(zawartosc_lodowki)[0][0]
                    id_col = np.nonzero(zawartosc_lodowki)[1][0]
                    jedzony_produkt = self.lista_produktow[id_col]
                    zawartosc_lodowki[id_row][id_col] = 0
                    kalorycznosc = jedzony_produkt[1]
                    aktualne_zuzycie += kalorycznosc
                    aktualny_stan_lodowki -= 1
                else:
                    wiersz_copy.bilans += aktualne_zuzycie - self.zapotrz_kal  # aktualizacja bilansu kalorii (zaznaczenie niedoboru)
                    break

            init_solution[-1] = wiersz_copy
        # print(init_solution)
        # print('lista_prod', self.lista_produktow)
        return init_solution

    def check_kalorie(self):
        """
        Metoda sprawdza czy produkty, które w danym dniu wybraliśmy spełniają nasze
        ograniczenie dotyczące zapotrzebowania dziennego na kalorie.

        Jeśli niedobor w danym dniu czyli (suma kaloryczności poszczególnych
        produktów) - (zapotrzebowanie dzienne) <  0 to wtedy wybieramy produkty o
        najmniejszej możliwej wadze dopóki niedobór będzie większy od 0.
        note: w tym momencie nie sprawdzamy czy po dadaniu produktu przekroczyliśmy
        maksymalna dopuszczalna pojemnosc plecaka max_poj_plecaka
        """
        for i in range(len(self.initial_solution)):
            if self.initial_solution[i].bilans < 0:  # jeśli niedobor jest mniejszy od 0
                self.initial_solution[i].decyzja = 1  # trzeba bedzie pojsc na zakupy
                lista_zakupow = self.initial_solution[i].lista_produktow
                stan_plecaka = 0
                produkty_do_wziecia = copy.deepcopy(self.lista_produktow)
                for j in range(len(lista_zakupow)):
                    stan_plecaka += lista_zakupow[j] * self.lista_produktow[j][0]
                    if lista_zakupow[j] == 1:  # Bierzemy dany produkt jeśli 1
                        produkty_do_wziecia[j][0] = self.max_poj_plecaka + 1  # Zabronione przejscie

                # tym kroku spradzamy ponownie czy po wybraniu w pierwszej turze
                # x produktów i ich sumaryczna kaloryczność < zapotrzebowanie dzienne
                # to wtedy bierzemy n produktów o najmniejszej możliwej dopuszczalnej
                # masie tak aby sumaryczna_kalorycznosć >= zapotrzebowanie_dzienne
                niedobor = self.initial_solution[i].bilans
                while niedobor < 0:
                    min_waga = np.min(produkty_do_wziecia[:, 0])
                    itemindex = np.where(produkty_do_wziecia[:, 0] == min_waga)[0][0]
                    self.initial_solution[i].lista_produktow[itemindex] = 1
                    niedobor += produkty_do_wziecia[itemindex][1]
                    produkty_do_wziecia[itemindex][0] = self.max_poj_plecaka + 1
                self.initial_solution[i].bilans = 0
            else:
                continue

    def step1(self, macierz_pom_produktow=None):
        """
        Generowanie sąsiednich rozwiązan
        """
        macierz_pom_produktow2 = np.empty((len(self.initial_solution), 10))
        if macierz_pom_produktow is None:
            # macierz_pom_produktow2 = np.empty((len(self.initial_solution), 10))
            for i in range(0, len(self.initial_solution)):
                macierz_pom_produktow2[i] = self.initial_solution[i].lista_produktow
        else:
            macierz_pom_produktow2 = copy.deepcopy(macierz_pom_produktow)
        # Zamień miejscami 5 losowo wybranych produktów
        for i in range(50):
            kierunek_przesuniecia = [1, 2, 3, 4]  # 1 - gora, 2 - dol, 3-lewo, 4-
            x_idx = np.random.randint(0, macierz_pom_produktow2.shape[1])
            y_idx = np.random.randint(0, macierz_pom_produktow2.shape[0])
            # print(x_idx, y_idx)
            if x_idx == 0:
                kierunek_przesuniecia.remove(4)
            elif x_idx == macierz_pom_produktow2.shape[1] - 1:
                kierunek_przesuniecia.remove(2)

            if y_idx == 0:
                kierunek_przesuniecia.remove(1)

            elif y_idx == macierz_pom_produktow2.shape[0] - 1:
                kierunek_przesuniecia.remove(3)

            kierunek_przesuniecia_wybor = random.choice(kierunek_przesuniecia)
            # print(kierunek_przesuniecia_wybor)
            if kierunek_przesuniecia_wybor == 1:  # gora
                macierz_pom_produktow2[y_idx, x_idx], macierz_pom_produktow2[y_idx - 1, x_idx] = macierz_pom_produktow2[
                                                                                                     y_idx - 1, x_idx], \
                                                                                                 macierz_pom_produktow2[
                                                                                                     y_idx, x_idx]
            elif kierunek_przesuniecia_wybor == 3:  # dol
                macierz_pom_produktow2[y_idx, x_idx], macierz_pom_produktow2[y_idx + 1, x_idx] = macierz_pom_produktow2[
                                                                                                     y_idx + 1, x_idx], \
                                                                                                 macierz_pom_produktow2[
                                                                                                     y_idx, x_idx]

            elif kierunek_przesuniecia_wybor == 2:  # prawo
                macierz_pom_produktow2[y_idx, x_idx], macierz_pom_produktow2[y_idx, x_idx + 1] = macierz_pom_produktow2[
                                                                                                     y_idx, x_idx + 1], \
                                                                                                 macierz_pom_produktow2[
                                                                                                     y_idx, x_idx]
            else:  # lewo
                macierz_pom_produktow2[y_idx, x_idx], macierz_pom_produktow2[y_idx, x_idx - 1] = macierz_pom_produktow2[
                                                                                                     y_idx, x_idx - 1], \
                                                                                                 macierz_pom_produktow2[
                                                                                                     y_idx, x_idx]

        # self.tabu_list.append(copy.deepcopy(macierz_pom_produktow))

        return macierz_pom_produktow2

    def check_weight(self, macierz_pom_produktow: np.ndarray) -> List[bool]:
        """
        jako parametr przyjmuje macierz w której wiersze reprezentują kolejne dni, natomiast
        kolumny listę produktów
        Zwraca List[bool] informujaca czy w danym dniu zakres plecaka został przekroczony
        """
        ponad_stan_lst = []
        for row in range(len(macierz_pom_produktow)):
            waga = 0
            for col in range(len(macierz_pom_produktow[row])):
                waga += macierz_pom_produktow[row][col] * self.lista_produktow[col][0]

            if waga > self.max_poj_plecaka:
                ponad_stan_lst.append(True)

            else:
                ponad_stan_lst.append(False)

        return ponad_stan_lst

    def check_capacity(self, macierz_pom_produktow2):
        """
        jako parametr przyjmuje macierz w której wiersze reprezentują kolejne dni, natomiast
        kolumny listę produktów
        Zwraca List informujaca czy w danym dniu zakres lodowki został przekroczony
        """
        if isinstance(macierz_pom_produktow2[0], ds.Solution):
            macierz_pom_produktow2 = np.empty((len(self.initial_solution), 10))
            for i in range(0, len(self.initial_solution)):
                macierz_pom_produktow2[i] = self.initial_solution[i].lista_produktow

        ponad_stan_lst_lodowka = []
        bilans_kalorie = []
        aktualny_stan_lodowki = self.poczatkowy_stan_lodowki
        zawartosc_lodowki = []
        for row in range(len(macierz_pom_produktow2)):

            # print("nowy dzien, lista zakupow")
            # print(macierz_pom_produktow2[row])
            if not all([v == 0 for v in macierz_pom_produktow2[row]]):
                zawartosc_lodowki.append(macierz_pom_produktow2[row])
                aktualny_stan_lodowki += sum(macierz_pom_produktow2[row])

                # print("dodaje ", sum(macierz_pom_produktow2[row]), " produktow")

                ponad_stan_lst_lodowka.append(aktualny_stan_lodowki)

            aktualne_zuzycie = 0
            bilans_kalorie.append(0)
            while aktualne_zuzycie < self.zapotrz_kal:
                if (len(np.nonzero(zawartosc_lodowki)[0])) > 0:
                    # print(zawartosc_lodowki)
                    # print(np.nonzero(zawartosc_lodowki))
                    id_row = np.nonzero(zawartosc_lodowki)[0][0]
                    id_col = np.nonzero(zawartosc_lodowki)[1][0]
                    jedzony_produkt = self.lista_produktow[id_col]

                    zawartosc_lodowki[id_row][id_col] = 0
                    # if all([v == 0 for v in zawartosc_lodowki[0]]):
                    #   if len(zawartosc_lodowki)==1:
                    #     zawartosc_lodowki = np.zeros((1, 10))
                    #   else:
                    #     zawartosc_lodowki = np.delete(zawartosc_lodowki, 0, 0)
                    kalorycznosc = jedzony_produkt[1]
                    aktualne_zuzycie += kalorycznosc
                    aktualny_stan_lodowki -= 1

                    # print("usuwam 1 produkt")

                else:
                    bilans_kalorie.append(aktualne_zuzycie - self.zapotrz_kal)
                    break

        return ponad_stan_lst_lodowka, bilans_kalorie

    def check_current_sol_in_tabu_list(self, list_of_sol: List[np.ndarray], current_solution: np.ndarray) -> bool:
        """
        Sprawdza czy obecne rozwiązanie jest w tabu list zwraca True jeśli tak
        """
        return next((True for elem in self.tabu_list if elem is current_solution), False)

    def zwroc_najlepsze_rozwiazanie(self, initial_solution):
        min = 0
        for i in range(len(initial_solution)):
            min += initial_solution[i].decyzja
        return min

    def zwroc_liste_produktow(self, macierz_pom_produktow=None):
        # print("xd", macierz_pom_produktow)
        if macierz_pom_produktow is not None and isinstance(macierz_pom_produktow, np.ndarray):
            macierz_pom_produktow2 = np.empty((len(macierz_pom_produktow), 10))
            for i in range(0, len(macierz_pom_produktow)):
                tmp = macierz_pom_produktow[i]
                # print('temp\t', tmp)
                for j in range(0, len(macierz_pom_produktow[0])):
                    macierz_pom_produktow2[i][j] = tmp[j]
            return macierz_pom_produktow2

        else:
            macierz_pom_produktow = np.empty((len(self.initial_solution), 10))
            for i in range(0, len(self.initial_solution)):
                macierz_pom_produktow[i] = self.initial_solution[i].lista_produktow
            return macierz_pom_produktow

    def postac_do_rozwiazania(self, lista_produktow) -> List[ds.Solution]:
        lista = copy.deepcopy(lista_produktow)
        rozwiazanie = []
        bilans = self.check_capacity(lista)[1]
        for i in range(len(lista_produktow)):
            decyzja = 1
            if all([v == 0 for v in lista_produktow[i]]):
                decyzja = 0
            solution = ds.Solution(decyzja, lista_produktow[i], bilans[i])
            rozwiazanie.append(solution)
        return rozwiazanie

    def print_solution(self, solution: List[ds.Solution]):
        S = ''
        for elem in solution:
            S += f"{elem}\n"
        print(S)

    def tabu_solution(self):
        it = 0
        lista_produktow_poczatkowa = self.zwroc_liste_produktow()
        self.tabu_list.append(lista_produktow_poczatkowa)
        print("Poczatkowe najlepsze rozwiazanie",
              self.zwroc_najlepsze_rozwiazanie(self.postac_do_rozwiazania(lista_produktow_poczatkowa)))
        # print("AXDDDDD", self.postac_do_rozwiazania(lista_produktow_poczatkowa))
        self.print_solution(self.postac_do_rozwiazania(lista_produktow_poczatkowa))
        # print("przed while", it)
        poprzednie_rozwiazanie = self.zwroc_liste_produktow()

        while it < self.kryterium_stopu:
            it += 1
            # print("Po while", it)
            copy_for_step = copy.deepcopy(poprzednie_rozwiazanie)
            sasiednie_rozwiazanie = self.step1(copy_for_step)
            # self.check_kalorie()
            sasiednie_rozwiazanie = self.zwroc_liste_produktow(sasiednie_rozwiazanie)

            for_check = copy.deepcopy(sasiednie_rozwiazanie)
            sasiednie_rozwiazanie_lodowka_ponad_stan, kalorie_sasiednie_rozwiazanie = self.check_capacity(
                macierz_pom_produktow2=for_check)

            if self.check_current_sol_in_tabu_list(self.tabu_list, for_check):
                print("rozw w liscie tabu \t", it)
                continue

            elif any([v > self.maksymalna_poj_lodowki for v in sasiednie_rozwiazanie_lodowka_ponad_stan]) or any(
                    [v < 0 for v in kalorie_sasiednie_rozwiazanie]):
                if any([v < 0 for v in kalorie_sasiednie_rozwiazanie]):
                    print("wykrylo ze jest nie ok kcal")
                else:
                    print("wykrylo ze jest nie ok else")
                self.tabu_list.append(for_check)
                continue

            else:
                print("rowz NIE w liscie tabu \t", it)
                rozwiazanie = self.postac_do_rozwiazania(sasiednie_rozwiazanie)
                best_current_sol = self.zwroc_najlepsze_rozwiazanie(rozwiazanie)
                print("rozwiazanie_poprzednie: ", rozwiazanie)
                poprzednie_rozwiazanie = self.zwroc_liste_produktow(rozwiazanie)

                if self.zwroc_najlepsze_rozwiazanie(self.best_solution) > best_current_sol:
                    print("Najlepsze rozwiazanie\t: ", best_current_sol)
                    # print(rozwiazanie)
                    self.print_solution(solution=rozwiazanie)
                    self.best_solution = rozwiazanie
                    print("Kolejne rozwiazania: \t", best_current_sol)
                    print(rozwiazanie)
                else:
                    print("NIE najlepsze rozwiazanie\t", best_current_sol)
                    # print(rozwiazanie)
                    self.print_solution(rozwiazanie)
                    continue

    # def __str__(self):
    # # coś nie działa ogarnać poprawne wyświetlanie
    #     result = ""
    #
    #     for elem in self.initial_solution:
    #         result += f"{elem}"
    #     return result
