import csv
import math
import re
import os
from functools import reduce

from prettytable import PrettyTable, ALL

dic_transl = {'name': 'Название',
              'description': 'Описание',
              'key_skills': 'Навыки',
              'experience_id': 'Опыт работы',
              'premium': 'Премиум-вакансия',
              'employer_name': 'Компания',
              'salary_from': 'Нижняя граница вилки оклада',
              'salary_to': 'Верхняя граница вилки оклада',
              'salary': 'Оклад',
              'salary_gross': 'Оклад указан до вычета налогов',
              'salary_currency': 'Идентификатор валюты оклада',
              'area_name': 'Название региона',
              'published_at': 'Дата публикации вакансии',
              '№': '№',
              'noExperience': 'Нет опыта',
              'between1And3': 'От 1 года до 3 лет',
              'between3And6': 'От 3 до 6 лет',
              'moreThan6': 'Более 6 лет',
              'False': 'Нет',
              'True': 'Да',
              'AZN': 'Манаты',
              'BYR': 'Белорусские рубли',
              'EUR': 'Евро',
              'GEL': 'Грузинский лари',
              'KGS': 'Киргизский сом',
              'KZT': 'Тенге',
              'RUR': 'Рубли',
              'UAH': 'Гривны',
              'USD': 'Доллары',
              'UZS': 'Узбекский сум'}


def main():
    list_naming, data_vacancies = read_file(input())  # input()
    if len(list_naming) == 0:
        print("Пустой файл")
    elif len(data_vacancies) == 0:
        print("Нет данных")
    else:
        data_vacancies = csv_filer(data_vacancies, list_naming)
        parameters = input()
        num = input()
        name = input()
        if not check_paramtrs(parameters):
            return
        data_vacancies = data_filter(data_vacancies, parameters)
        num_str = num.split(' ')
        name_colm = name.split(', ')
        if data_vacancies:
            table = create_table(data_vacancies)
            print(cut_table(table, num_str, name_colm))
        else:
            print('Ничего не найдено')


def check_paramtrs(parameters):
    if len(parameters) == 0:
        return True
    parameters_list = parameters.split(': ')
    if ':' not in parameters:
        print('Формат ввода некорректен')
        return False
    if parameters[:parameters.index(':')] not in dic_transl.values():
        print('Параметр поиска некорректен')
        return False
    parameters_list[0] = ''.join(filter(lambda x: parameters_list[0] == dic_transl[x], dic_transl))
    return bool(parameters_list[0])


def data_filter(data_vacancies, parameters):
    if len(parameters) == 0:
        return data_vacancies
    parameters_list = parameters.split(': ')
    data = []
    parameters_list[0] = ''.join(filter(lambda x: parameters_list[0] == dic_transl[x], dic_transl))
    i = ''.join(filter(lambda x: parameters_list[1] == dic_transl[x], dic_transl))
    if i:
        parameters_list[1] = i
    if parameters_list[0] == 'key_skills':
        parameters_list[1] = parameters_list[1].split(', ')
        for vacancy in data_vacancies:
            f = True
            for parametr in parameters_list[1]:
                if parametr not in vacancy[parameters_list[0]]:
                    f = False
            if f:
                data.append(vacancy)
    elif parameters_list[0] == 'salary':
        for vacancy in data_vacancies:
            if float(vacancy['salary_from']) <= float(parameters_list[1]) <= float(vacancy['salary_to']):
                data.append(vacancy)
    elif parameters_list[0] == 'published_at':
        for vacancy in data_vacancies:
            if f"{vacancy['published_at'][8:10]}.{vacancy['published_at'][5:7]}.{vacancy['published_at'][:4]}" == \
                    parameters_list[1]:
                data.append(vacancy)
    else:
        for vacancy in data_vacancies:
            if parameters_list[1] == vacancy[parameters_list[0]]:
                data.append(vacancy)
    return data


def cut_table(table, num_str, name_colm):
    if len(num_str) == 1:
        return table.get_string(start=0 if num_str[0] == '' else int(num_str[0]) - 1,
                                fields=table.field_names if name_colm[0] == '' else ['№'] + name_colm)
    else:
        return table.get_string(start=int(num_str[0]) - 1, end=int(num_str[1]) - 1,
                                fields=table.field_names if name_colm[0] == '' else ['№'] + name_colm)


def translate(list_naming):
    list_translate = []
    for name in list_naming:
        list_translate.append(dic_transl[name])
    return list_translate


def create_table(data_vacancies):
    data = []
    for i, vacincie in enumerate(data_vacancies):
        data.append(vacincie)
        data[i] = formatter(vacincie)
        data[i]['key_skills'] = data_vacancies[i]['key_skills']
    table = PrettyTable()
    table.field_names = ['№'] + translate(list(data[0].keys()))
    table.hrules = ALL
    table.align = 'l'
    table.max_width = 20
    for i, row in enumerate(data):
        row['key_skills'] = reduce(lambda x, y: x + '\n' + y, row['key_skills'])
        if len(row['key_skills']) > 100:
            row['key_skills'] = row['key_skills'][:100] + '...'
        if len(row['description']) > 100:
            row['description'] = row['description'][:100] + '...'
        table.add_row([i + 1] + list(row.values()))
    return table


def print_vacancies(data_vacancies, dic_name):
    for i, vacancy in enumerate(data_vacancies):
        data_vacancies[i] = formatter(vacancy)
        for item in data_vacancies[i]:
            print(f"{dic_name[item]}: {data_vacancies[i][item]}")
        print()


def print_data(date, data_salary_min, data_skills, data_area):
    if len(date) < 10:
        size = len(date)
    else:
        size = 10
    print('Самые высокие зарплаты:')
    for i in range(0, size):
        if date[i]['salary_average'] % 10 == 1:
            rur = 'рубль'
        elif 1 < date[i]['salary_average'] % 10 < 5:
            rur = 'рубля'
        else:
            rur = 'рублей'
        print(
            f"""    {i + 1}) {date[i]['name']} в компании "{date[i]['employer_name']}" - {date[i]['salary_average']} {rur} (г. {date[i]['area_name']})""")

    print('\nСамые низкие зарплаты:')

    for i in range(0, size):
        if data_salary_min[i]['salary_average'] % 10 == 1:
            rur = 'рубль'
        elif 1 < data_salary_min[i]['salary_average'] % 10 < 5:
            rur = 'рубля'
        else:
            rur = 'рублей'
        print(
            f"""    {i + 1}) {data_salary_min[i]['name']} в компании "{data_salary_min[i]['employer_name']}" - {data_salary_min[i]['salary_average']} {rur} (г. {data_salary_min[i]['area_name']})""")

    print(f'\nИз {len(data_skills)} скиллов, самыми популярными являются:')
    for i in range(0, 10 if len(data_skills) > 10 else len(data_skills)):
        if data_skills[i][1] % 10 == 1 or data_skills[i][1] % 10 == 0 or 4 < data_skills[i][1] % 100 < 22 or 4 < \
                data_skills[i][1] % 10 < 9:
            ras = 'раз'
        else:
            ras = 'раза'
        print(
            f"""    {i + 1}) {data_skills[i][0]} - упоминается {data_skills[i][1]} {ras}""")

    print(f'\nИз {len(data_area)} городов, самые высокие средние ЗП:')
    counter = 0
    i = 0
    while counter != 10 and i < len(date):
        if data_area[i][2] >= math.floor(len(date) / 100):
            if 4 < data_area[i][2] < 21 or data_area[i][2] % 10 > 4:
                vac = 'вакансий'
            elif data_area[i][2] % 10 == 1:
                vac = 'вакансия'
            else:
                vac = 'вакансии'
            if data_area[i][1] % 10 == 1:
                rur = 'рубль'
            elif 1 < data_area[i][1] % 10 < 5 and not 9 < data_area[i][1] % 100 < 21:
                rur = 'рубля'
            else:
                rur = 'рублей'
            print(
                f"""    {counter + 1}) {data_area[i][0]} - средняя зарплата {data_area[i][1]} {rur} ({data_area[i][2]} {vac})""")
            counter += 1
        i += 1


def formatter(row):
    dict_new = {}
    dict_new['name'] = row['name']
    dict_new['description'] = row['description']
    dict_new['key_skills'] = ', '.join(row['key_skills'])
    dict_new['experience_id'] = dic_transl[row['experience_id']]
    dict_new['premium'] = 'Да' if (row['premium'] == 'True') else 'Нет'
    dict_new['employer_name'] = row['employer_name']
    salary_from = "{0:,}".format((int(float(row['salary_from'])))).replace(',', ' ')
    salary_to = "{0:,}".format((int(float(row['salary_to'])))).replace(',', ' ')
    dict_new[
        'salary'] = f"{salary_from} - {salary_to} ({dic_transl[row['salary_currency']]}) ({'С вычетом' if row['salary_gross'] == 'False' else 'Без вычета'} налогов)"
    dict_new['area_name'] = row['area_name']
    dict_new['published_at'] = f"{row['published_at'][8:10]}.{row['published_at'][5:7]}.{row['published_at'][:4]}"
    return dict_new


def take_area(main_data):
    data = {}
    data_sort = []
    for vacancy in main_data:
        if data.__contains__(vacancy['area_name']):
            data[vacancy['area_name']] = [(int(vacancy['salary_average']) + int(data[vacancy['area_name']][0])),
                                          data[vacancy['area_name']][1] + 1]
        else:
            data[vacancy['area_name']] = [int(vacancy['salary_average']), 1]
    for key in data:
        data_sort.append([key, math.floor(data[key][0] / data[key][1]), data[key][1]])
    data_sort = sorted(data_sort, key=lambda x: int(x[1]), reverse=True)
    return data_sort


def take_skills(main_data):
    data = []
    data_dict = {}
    for skills in map(lambda x: x['key_skills'], main_data):
        for skill in skills:
            if skill not in data_dict:
                data_dict[skill] = 1
            else:
                data_dict[skill] += 1
    for skill in data_dict:
        data.append([skill, data_dict[skill]])
    return sorted(data, key=lambda x: x[1], reverse=True)


def salary_sort(main_data, reverse=True):
    data = []
    data_sal = []
    for i, row in enumerate(main_data):
        data_sal.append([row['salary_average'], i])
    data_sal = sorted(data_sal, key=lambda x: int(x[0]), reverse=reverse)
    for row in data_sal:
        data.append(main_data[row[1]])
    return data


def read_file(name):
    if os.stat(name).st_size == 0:
        return [], []
    flag = True
    counter = 0
    data = []
    with open(name, encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        heading = next(reader)
        data.append(heading)
        for row in reader:
            for piece in row:
                if len(piece) == 0:
                    flag = False
                counter += 1
            if flag and (len(heading) == counter):
                data.append(row)
            flag = True
            counter = 0
    list_naming = data[0]
    data.pop(0)
    return list_naming, data


def csv_filer(data, list_naming):
    pattern = re.compile('<.*?>')
    pattern1 = re.compile('\s+')
    data_new = []
    for row in data:
        dict_new = {}
        for i in range(0, len(list_naming)):
            if list_naming[i] == 'key_skills':
                dict_new[list_naming[i]] = row[i].split("\n")
            else:
                # row[i] = row[i].replace("\n", ", ")
                row[i] = re.sub(pattern, '', row[i])
                row[i] = re.sub(pattern1, ' ', row[i])
                row[i] = row[i].strip()
                dict_new[list_naming[i]] = row[i]
        dict_new['salary_average'] = math.floor(
            (int(dict_new['salary_from'].replace('.0', '')) + int(dict_new['salary_to'].replace('.0', ''))) / 2)
        data_new.append(dict_new)
    return data_new


if __name__ == "__main__":
    main()
