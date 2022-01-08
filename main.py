import numpy as np
import pandas as pd
import random
import copy
from typing import List


#dane
n_records = 10

tabela_produktow = [f"Produkt{i+1}" for i in range(n_records)]
print(tabela_produktow)

# tabele zczytywac z excela c(wartociowosc od wagi od czegos dodatkowego np kalorie)
# ograniczenie plecaka tez (czy robic funkcje ktora wylicza ktore dni sa niehandlowe (niedziele i swieta))



# tabela_wartosciowosc_kalorie = np.random.randint(low=400, high=1000, size=n_records)

tabela_wartosciowosc_kalorie = np.round(np.random.normal(1000, 300, size=n_records))
tabela_wartosciowosc_przydatnosc = np.random.randint(low=0, high=2, size=n_records)
tabela_wag = np.round(np.random.random(n_records) * 3, 2)

print(tabela_wartosciowosc_kalorie)
print(tabela_wartosciowosc_przydatnosc)
print(tabela_wag)


tabela_merge = {}
for i in range(len(tabela_produktow)):
  tabela_merge[tabela_produktow[i]] = [tabela_wag[i], tabela_wartosciowosc_kalorie[i], tabela_wartosciowosc_przydatnosc[i]]

# print(tabela_merge)

df = pd.DataFrame(tabela_merge).transpose()
df.rename(columns={0: "waga", 1: "kaloryczność", 2:"przydatnosc"})

print(df.to_numpy())




# Ograniczenia
class lodowka():
  poczatkowy_stan_lodowki = 0 # poczatkowy stan lodowki

  maksymalna_poj_lodowki = 20 # maksymalna ilosc produktow w lodowce
  maks_liczba = 1 # maksymalna ilosc tego samego produktu
  N = 365 #tbd
  max_poj_plecaka = 7 # kg maksymalna pojemnosc_plecaka
  zapotrz_kal = 3000 # Zapotrzebowanie kaloryczne w danym dniu - w każdym dniu tyle samo

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
    self.tabu_list = [] # Lista tabu

  def generete_initial_solution(self) -> np.ndarray:
    """
    Returns:
    initial_solution (list): Rozwiązanie początkowe, baza do kolejnych kroków.
    Kolejne elementy initial_solution oznaczają kolejne dni terminarza.
    Przykładowe elementy listy:
    [1, [0, 0, 1, 0, 0, 1, 0, 1, 1, 1], 0]
    [0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], -19.0]
    gdzie:  initial_solution[i][0]: decyzja o pójściu na zakupy
            initial_solution[i][1]: lista wziętych produktów
            initial_solution[i][2]: bilans kalorii

    """
    initial_solution = []  # Rozwiązanie początkowe
    self.lista_produktow = self.lista_produktow.to_numpy()
    aktualny_stan_lodowki = self.poczatkowy_stan_lodowki
    zawartosc_lodowki = []
    for i in range(len(self.terminarz)):
      aktualny_stan_plecaka = 0
      if self.terminarz[i][2] != 0:
        teoretyczna_lista_zakupow = random.sample(range(10), 10)
        lista_1 = [0]*len(self.lista_produktow)
        count = 0
        while True:
            indeks_produktu_ktory_bierzemy = teoretyczna_lista_zakupow[count]
            waga_produktu = self.lista_produktow[indeks_produktu_ktory_bierzemy][0]

            #sprawdzenie czy produkt który zamierzamy wziąć spełnia ograniczenia lodówki i plecaka:
            if aktualny_stan_lodowki + 1 <= self.maksymalna_poj_lodowki and aktualny_stan_plecaka + waga_produktu <= self.max_poj_plecaka:
              lista_1[indeks_produktu_ktory_bierzemy] = 1
              aktualny_stan_lodowki += 1
              aktualny_stan_plecaka += waga_produktu
              count += 1
            else:
              break

        initial_solution.append([1, lista_1 , 0])
        zawartosc_lodowki.append(lista_1)
      else:
        initial_solution.append([ 0, [0]*len(self.lista_produktow) , 0])

      #aktualizacja zużycia produktow (sprawdzenie w których dniach będzie niedobór kaloryczny (poprawiane następnie w check_kalorie())):
      aktualne_zuzycie = 0
      while aktualne_zuzycie < self.zapotrz_kal:
        if (len(zawartosc_lodowki)) > 0:
          jedzony_produkt = self.lista_produktow[np.nonzero(zawartosc_lodowki[0])[0][0]]
          if all([v == 0 for v in zawartosc_lodowki[0]]):
            zawartosc_lodowki[0].pop()
          kalorycznosc = jedzony_produkt[1]
          aktualne_zuzycie += kalorycznosc
          aktualny_stan_lodowki -= 1
        else:
          initial_solution[i][2] = aktualne_zuzycie - self.zapotrz_kal #aktualizacja bilansu kalorii (zaznaczenie niedoboru)
          break


      #           aktualne_zuzycie = 0
      # bilans_kalorie.append([0])
      # while aktualne_zuzycie < self.zapotrz_kal:
      #   if (len(zawartosc_lodowki)) > 0:
      #     # print(zawartosc_lodowki)
      #     # print(np.nonzero(zawartosc_lodowki))
      #     id_row = np.nonzero(zawartosc_lodowki)[0][0]
      #     id_col = np.nonzero(zawartosc_lodowki)[1][0]
      #     jedzony_produkt = self.lista_produktow[id_col]

      #     zawartosc_lodowki[id_row][id_col] = 0
      #     # if all([v == 0 for v in zawartosc_lodowki[0]]):
      #     #   if len(zawartosc_lodowki)==1:
      #     #     zawartosc_lodowki = np.zeros((1, 10))
      #     #   else:
      #     #     zawartosc_lodowki = np.delete(zawartosc_lodowki, 0, 0)
      #     kalorycznosc = jedzony_produkt[1]
      #     aktualne_zuzycie += kalorycznosc
      #     aktualny_stan_lodowki -= 1
      
      #     # print("usuwam 1 produkt")
      
      #   else:
      #     bilans_kalorie[row][0] = aktualne_zuzycie - self.zapotrz_kal
      #     break


    # lista = np.random.randint(0, 10, 10)
    # for i in range(len(initial_solution)):
    #   if initial_solution[i][0] != 0:
    #     for j in range(len(self.lista_produktow)):
    #       initial_solution[i][1].append(np.random.randint(0, 2)) #ewentualnie mozna brac wiecej (randint (0, x))

    # dorzucic na kazdy dzien liste produktow , uwzgledniajac ich zuzycie -> czy spelnia to zapotrzebowanie
    return initial_solution


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
      if self.initial_solution[i][2] < 0: # jeśli niedobor jest mniejszy od 0
        self.initial_solution[i][0] = 1 #trzeba bedzie pojsc na zakupy
        lista_zakupow = self.initial_solution[i][1]
        stan_plecaka = 0
        produkty_do_wziecia = copy.deepcopy(self.lista_produktow)
        for j in range(len(lista_zakupow)):
          stan_plecaka += lista_zakupow[j]*self.lista_produktow[j][0]
          if lista_zakupow[j] == 1: # Bierzemy dany produkt jeśli 1
            produkty_do_wziecia[j][0] = self.max_poj_plecaka+1 # Zabronione przejscie

        # tym kroku spradzamy ponownie czy po wybraniu w pierwszej turze
        # x produktów i ich sumaryczna kaloryczność < zapotrzebowanie dzienne
        # to wtedy bierzemy n produktów o najmniejszej możliwej dopuszczalnej
        # masie tak aby sumaryczna_kalorycznosć >= zapotrzebowanie_dzienne
        niedobor = self.initial_solution[i][2]
        while niedobor < 0:
          min_waga = np.min(produkty_do_wziecia[:, 0])
          itemindex = np.where(produkty_do_wziecia[:, 0]==min_waga)[0][0]
          self.initial_solution[i][1][itemindex] = 1
          niedobor += produkty_do_wziecia[itemindex][1]
          produkty_do_wziecia[itemindex][0] = self.max_poj_plecaka+1
        self.initial_solution[i][2] = 0
      else:
        continue


  def step1(self): 
    macierz_pom_produktow = np.empty((len(self.initial_solution), 10))
    for i in range(0, len(self.initial_solution)):
      macierz_pom_produktow[i] = self.initial_solution[i][1]  

    for i in range(10):
      kierunek_przesuniecia = [1, 2, 3, 4] # 1 - gora, 2 - dol, 3-lewo, 4- 
      x_idx = np.random.randint(0, macierz_pom_produktow.shape[1])
      y_idx = np.random.randint(0, macierz_pom_produktow.shape[0])
      print(x_idx, y_idx)
      if x_idx == 0: 
        kierunek_przesuniecia.remove(4)
      elif x_idx == macierz_pom_produktow.shape[1]-1:
        kierunek_przesuniecia.remove(2)

      if y_idx == 0:
        kierunek_przesuniecia.remove(1)

      elif y_idx == macierz_pom_produktow.shape[0]-1:
        kierunek_przesuniecia.remove(3)

      kierunek_przesuniecia_wybor = random.choice(kierunek_przesuniecia)
      print(kierunek_przesuniecia_wybor)
      if kierunek_przesuniecia_wybor == 1: #gora
        macierz_pom_produktow[y_idx,x_idx], macierz_pom_produktow[y_idx - 1,x_idx] = macierz_pom_produktow[y_idx - 1 ,x_idx], macierz_pom_produktow[y_idx ,x_idx]
      elif kierunek_przesuniecia_wybor == 3:#dol
        macierz_pom_produktow[y_idx,x_idx], macierz_pom_produktow[y_idx + 1,x_idx] = macierz_pom_produktow[y_idx + 1 ,x_idx], macierz_pom_produktow[y_idx ,x_idx]

      elif kierunek_przesuniecia_wybor == 2: # prawo
        macierz_pom_produktow[y_idx,x_idx], macierz_pom_produktow[y_idx ,x_idx + 1] = macierz_pom_produktow[y_idx ,x_idx + 1], macierz_pom_produktow[y_idx ,x_idx]
      else: #lewo
        macierz_pom_produktow[y_idx,x_idx], macierz_pom_produktow[y_idx ,x_idx - 1] = macierz_pom_produktow[y_idx ,x_idx - 1], macierz_pom_produktow[y_idx ,x_idx]

    self.tabu_list.append(copy.deepcopy(macierz_pom_produktow))
    return macierz_pom_produktow


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

  def check_capacity(self):
   

    """
    jako parametr przyjmuje macierz w której wiersze reprezentują kolejne dni, natomiast
    kolumny listę produktów
    Zwraca List informujaca czy w danym dniu zakres lodowki został przekroczony
    """
    macierz_pom_produktow2 = np.empty((len(self.initial_solution), 10))
    for i in range(0, len(self.initial_solution)):
      macierz_pom_produktow2[i] = self.initial_solution[i][1]  
      
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
      bilans_kalorie.append([0])
      while aktualne_zuzycie < self.zapotrz_kal:
        if (len(zawartosc_lodowki)) > 0:
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
          bilans_kalorie[row][0] = aktualne_zuzycie - self.zapotrz_kal
          break

    return ponad_stan_lst_lodowka, bilans_kalorie


  # def check_current_sol_in_tabu_list(self, current_solution: np.ndarray) -> bool:
  #   """
  #   Sprawdza czy obecne rozwiązanie jest w tabu list zwraca True jeśli tak
  #   """
  #   # if len(self.tabu_list) == 1:
  #   #   return current_solution is self.tabu_list[0]
    
  #   # else:
  #   #   for elem in self.tabu_list:
  #   #     if current_solution is elem:
  #   #       return True
  #   #     else:
  #   #       continue
  #   #   return False
  #   return next((True for elem in self.tabu_list if elem is current_solution), False)

  def check_current_sol_in_tabu_list(self, list_of_sol, current_solution: np.ndarray) -> bool:
    list_of_solution = []
    for elem in range(len(list_of_sol)):
        for i in range(len(list_of_sol[elem])):
            same_elem: bool = True
            for j in range(len(list_of_sol[elem][i])):
                if current_solution[i][j] != list_of_sol[elem][i][j]:
                    same_elem = False
                    break
                else:
                    same_elem = True
            if same_elem is False:
                break
        if same_elem is False:
            list_of_solution.append(False)
        else:
            list_of_solution.append(True)
    return any(list_of_solution)
        




# [p1, p2, p3, p4]
  # [1000, 1000, 2000, 500]
## [1, [1,1,0,1], 2500-3000=-500, [] ]
# piatek:
## [1, [0,0,1,1], ..., []]
# sobta:
# [0, [0,0,0,0]]
# poniedzialek
# [p1, p2, p3, p4]
  # [1000, 1000, 2000, 500]
  # [5, 5, 10, 7]
  # [1234] (kolejka)
## [1, [1,0,1,1], 4000-3000=----, [p4]]
# jezeli niedobór co do kalorycznosci
# jezeli nadmiar co do pojemnosci plecaka -> usuwamy najmniej kaloryczny produkt


# x0 = 0 # poczatkowy stan lodowki
# x_max = 10 # maksymalna ilosc produktow w lodowce w danym momencie
# x_1 = 1 # maksymalna ilosc tego samego produktu
# N = 365 #tbd
# max_poj_plecaka = 20 # kg maksymalna pojemnosc_plecaka
# zapotrz_kal = 3000 # Zapotrzebowanie kaloryczne w danym dniu - w każdym dniu tyle samo
# # Zakładamy, że w niedziele nie robimy zakupów

## dodane: mieisiac pierwszy
# lista_swiat = [(1, 1), (1, 6), (5, 1), (5, 3), (8, 15), (11, 1), (11, 11), (12, 25), (12, 26)]
# 1, 3, 2 - spełnia
# 1, 2 - spełnia > 3000



# funkcja
import calendar
import datetime

lista_swiat = [datetime.date(2022, 1, 1),
               datetime.date(2022, 1, 6),
               datetime.date(2022, 4, 17),
               datetime.date(2022, 4, 18),
               datetime.date(2022, 5, 1),
               datetime.date(2022, 5, 3),
               datetime.date(2022, 6, 5),
               datetime.date(2022, 6, 16),
               datetime.date(2022, 7, 15),
               datetime.date(2022, 11, 1),
               datetime.date(2022, 11, 11),
               datetime.date(2022, 12, 25),
               datetime.date(2022, 12, 26)]


def returncalendar(first_day, first_month, first_year, last_day, last_month, last_year) :
  #doesnt include the last day -> update po dodaniu days = 1 tak
  #lista dni iteruje od 0

  # wielkanoc_mth = input("Kiedy Wielkanoc: numer miesiąca")
  # wielkanoc_day = input("Kiedy Wielkanoc: numer dnia")
  # boze_cialo_mth = input("Kiedy Boże Ciało: numer miesiąca")
  # boze_cialo_day = input("Kiedy Boże Ciało: numer dnia")

 # roboczo zeby nie wpisywac
  wielkanoc_mth = 4
  wielkanoc_day = 17
  boze_cialo_mth = 6
  boze_cialo_day = 16


  # lista_swiat_here = lista_swiat.copy()
  # lista_swiat_here.append((int(wielkanoc_mth), int(wielkanoc_day)))
  # lista_swiat_here.append((int(boze_cialo_mth), int(boze_cialo_day)))
  # # print(lista_swiat_here)

  # lista_swiat_here.sort()
  # # print(lista_swiat_here)


  vector_days = []

  d0 = datetime.date(first_year, first_month, first_day)
  d1 = datetime.date(last_year, last_month, last_day)

  start_date = d0
  end_date = d1
  delta = datetime.timedelta(days=1)

  while start_date <= end_date:
    weight = lodowka.max_poj_plecaka
    if start_date.weekday() == 6:
      weight = 0

    if start_date in lista_swiat:
      weight = 0  # poj plecaka

    vector_days.append((start_date, start_date.weekday(), weight))

    start_date += delta

  return vector_days


terminarz = returncalendar(3, 1, 2022, 31, 1, 2022)
# for i in range(len(terminarz)):
#   print(terminarz[i], '\n')




l1 = lodowka(terminarz, df)
sum = 0
for i in range(len(l1.initial_solution)):
  sum += l1.initial_solution[i][0]
  # print(l1.initial_solution[0][i])

# print(sum)
l1.check_kalorie()
print('\n')
sum = 0
for i in range(len(l1.initial_solution)):
  sum += l1.initial_solution[i][0]
  # print(sum(l1.initial_solution[0][i]))
# print(sum)
# to_print = l1.step1()
# print(to_print)
# to_print2 = l1.step1()


print(l1.check_capacity())