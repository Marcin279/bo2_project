import src.data_structures as ds
import src.tabu_solution as tsol


# import numpy as np

def test_solution_structures():
    # OK
    d = 1
    prod = np.random.randint(0, 2, 10)
    bilans = 456.1
    sol = ds.Solution(d, prod, bilans)
    print(sol)


def test_tabu_solution():
    terminarz = ds.return_calendar(3, 1, 2022, 15, 1, 2022)
    lista_produktow = ds.generuj_liste_produktow()

    lod1 = tsol.Lodowka(terminarz, lista_produktow)
    lod1.tabu_solution()


if __name__ == '__main__':
    # print(ds.return_calendar(3, 1, 2022, 15, 1, 2022))
    # test_solution_structures()

    test_tabu_solution()
