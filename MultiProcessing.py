import concurrent.futures
import time
from multiprocessing import Pool
import os
from os.path import isfile, join
from PrintOrCreate import DataSet, Statistics


def formate_result(response):
    """
    Собирает данные из потоков в нужный формат и выводит их на экран
    Args:
        response(list): данные врзврашенные потоками

    """
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
    # print_statics([dict_salary,
    #                dict_quantity,
    #                dict_salary_name,
    #                dict_quantity_name])


def print_statics(stats):
    """
    Выодит данные в необходимом формате
    Args:
        stats(list): данные для вывода на экран
    """
    print(f'Динамика уровня зарплат по годам: {stats[0]}')
    print(f'Динамика количества вакансий по годам: {stats[1]}')
    print(f'Динамика уровня зарплат по годам для выбранной профессии: {stats[2]}')
    print(f'Динамика количества вакансий по годам для выбранной профессии: {stats[3]}')


def main():
    """
    Основной метод которые запускает три различных метода получения данныех и собирает данные
    """
    x = []
    y = []
    z = []
    names = [f for f in os.listdir('F:/Makarov/Spilt_csv') if isfile(join('F:/Makarov/Spilt_csv', f))]
    for i in range(30):
        names = [f for f in os.listdir('F:/Makarov/Spilt_csv') if isfile(join('F:/Makarov/Spilt_csv', f))]
        start = time.time()
        vacancies = DataSet('vacancies_by_year.csv')
        stat = Statistics(vacancies)
        # print_statics(stat.salaryStat('Программист'))
        print(f'mono {time.time() - start} sec', end='\n\n')
        x.append(time.time() - start)
        start = time.time()
        with Pool() as p:
            p.map_async(read_split, names, callback=formate_result)
            p.close()
            p.join()
        # print(f'multi {time.time() - start} sec', end='\n\n')
        y.append(time.time() - start)
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            formate_result(executor.map(read_split, names))
        # print(f'concurrent.futures {time.time() - start} sec')
        z.append(time.time() - start)
    print(f'x = {x}')
    print(f'y = {y}')
    print(f'z = {z}')


def read_split(name):
    """
    Читает данные из переданного csv файла
    Args:
        name(str): название файла
    Returns:
         list = возврашает отсортированные в классе Statistics данные
    """
    stat = Statistics(DataSet(f'F:/Makarov/Spilt_csv/{name}'))
    return stat.salaryStat('Программист')


if __name__ == "__main__":
    main()
