import numpy as np
import datetime
import pandas as pd
from typing import List


# class Calendar:
#
#     def __init__(self, first_day, first_month, first_year, last_day, last_month, last_year):
#         self.first_day = first_day
#         self.first_month = first_month
#         self.first_year = first_year
#         self.last_day = last_day
#         self.last_month = last_month
#         self.last_year = last_year
#
#     def return_calendar(self):
#
#         vector_days = []
#
#         d0 = datetime.date(first_year, first_month, first_day)
#         d1 = datetime.date(last_year, last_month, last_day)
#
#         start_date = d0
#         end_date = d1
#         delta = datetime.timedelta(days=1)
#
#         while start_date <= end_date:
#             weight = lodowka.max_poj_plecaka
#             # if start_date.weekday() == 6:
#             #   weight = 0
#
#             if start_date in lista_swiat:
#                 weight = 0  # poj plecaka
#
#             vector_days.append((start_date, start_date.weekday(), weight))
#
#             start_date += delta
#
#         return vector_days


class Ograniczenia:
    poczatkowy_stan_lodowki = 0  # poczatkowy stan lodowki

    maksymalna_poj_lodowki = 20  # maksymalna ilosc produktow w lodowce
    maks_liczba = 1  # maksymalna ilosc tego samego produktu
    N = 365  # tbd
    max_poj_plecaka = 7  # kg maksymalna pojemnosc_plecaka
    zapotrz_kal = 3000  # Zapotrzebowanie kaloryczne w danym dniu - w każdym dniu tyle samo
    kryterium_stopu = 100  # maksymalna ilosc iteracji


class Solution:
    def __init__(self, decyzja: int, lista_produktow: List[int], bilans: float):
        self.decyzja = decyzja
        self.lista_produktow = lista_produktow
        self.bilans = bilans

    def __str__(self):
        return f"d:{self.decyzja} lst: {self.lista_produktow} b: {self.bilans}"

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.lista_produktow)


# lista_swiat = [datetime.date(2022, 1, 1),
#                datetime.date(2022, 1, 6),
#                datetime.date(2022, 4, 17),
#                datetime.date(2022, 4, 18),
#                datetime.date(2022, 5, 1),
#                datetime.date(2022, 5, 3),
#                datetime.date(2022, 6, 5),
#                datetime.date(2022, 6, 16),
#                datetime.date(2022, 7, 15),
#                datetime.date(2022, 11, 1),
#                datetime.date(2022, 11, 11),
#                datetime.date(2022, 12, 25),
#                datetime.date(2022, 12, 26)]
lista_swiat = []


def return_calendar(first_day, first_month, first_year, last_day, last_month, last_year):
    # doesnt include the last day -> update po dodaniu days = 1 tak
    # lista dni iteruje od 0

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
        weight = Ograniczenia.max_poj_plecaka
        # if start_date.weekday() == 6:
        #   weight = 0

        if start_date in lista_swiat:
            weight = 0  # poj plecaka

        vector_days.append((start_date, start_date.weekday(), weight))

        start_date += delta

    return vector_days


def generuj_liste_produktow():
    # dane
    n_records = 10

    tabela_produktow = [f"Produkt{i + 1}" for i in range(n_records)]

    # tabele zczytywac z excela c(wartociowosc od wagi od czegos dodatkowego np kalorie)
    # ograniczenie plecaka tez (czy robic funkcje ktora wylicza ktore dni sa niehandlowe (niedziele i swieta))

    tabela_wartosciowosc_kalorie = np.round(np.random.normal(1000, 300, size=n_records))
    tabela_wartosciowosc_przydatnosc = np.random.randint(low=0, high=2, size=n_records)
    tabela_wag = np.round(np.random.random(n_records) * 0.7, 2)
    tabela_merge = {}
    for i in range(len(tabela_produktow)):
        tabela_merge[tabela_produktow[i]] = [tabela_wag[i], tabela_wartosciowosc_kalorie[i],
                                             tabela_wartosciowosc_przydatnosc[i]]

    df = pd.DataFrame(tabela_merge).transpose()
    df.rename(columns={0: "waga", 1: "kaloryczność", 2: "przydatnosc"})

    return df
