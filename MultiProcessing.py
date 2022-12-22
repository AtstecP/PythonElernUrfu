import multiprocessing
import time
from functools import reduce
from multiprocessing import Pool
import multiprocessing
from multiprocessing import Pool
import os
from os.path import isfile, join

from matplotlib import pyplot as plt

from PrintOrCreate import DataSet, Statistics


def formate_result(response):
    dict_salary = {}
    dict_quantity = {}
    dict_salary_name = {}
    dict_quantity_name = {}
    for item in response:
        key = next(iter(item[0]))
        dict_salary[key] = item[0][key]
        dict_quantity[key] = item[1][key]
        dict_salary_name[key] = item[2][key]
        dict_quantity_name[key] = item[3][key]
    print_statics([dict_salary,
                   dict_quantity,
                   dict_salary_name,
                   dict_quantity_name])


def print_statics(stats):
    print(f'Динамика уровня зарплат по годам: {stats[0]}')
    print(f'Динамика количества вакансий по годам: {stats[1]}')
    print(f'Динамика уровня зарплат по годам для выбранной профессии: {stats[2]}')
    print(f'Динамика количества вакансий по годам для выбранной профессии: {stats[3]}')


def main():
    names = [f for f in os.listdir('F:/Makarov/Spilt_csv') if isfile(join('F:/Makarov/Spilt_csv', f))]
    start = time.time()
    vacancies = DataSet('vacancies_by_year.csv')
    stat = Statistics(vacancies)
    print_statics(stat.salaryStat('Программист'))
    print(f'mono {time.time() - start} sec', end='\n\n')
    start = time.time()
    with Pool(len(names)) as p:
        p.map_async(read_split, names, callback=formate_result)
        p.close()
        p.join()
    print(f'multi {time.time() - start} sec')


def read_split(name):
    stat = Statistics(DataSet(f'F:/Makarov/Spilt_csv/{name}'))
    return stat.salaryStat('Программист')


if __name__ == "__main__":
    main()
