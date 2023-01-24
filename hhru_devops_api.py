import csv
import time
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

import pandas as pd
import requests

def clean_vacancy(vacancy):
    if vacancy['salary'] == None:
        vacancy['salary'] = 'Нет данных'
    elif vacancy['salary']['from'] != None and vacancy['salary']['to'] != None and vacancy['salary']['from'] != vacancy['salary']['to']:
        vacancy['salary'] = f"от {'{0:,}'.format(vacancy['salary']['from']).replace(',', ' ')} до {'{0:,}'.format(vacancy['salary']['to']).replace(',', ' ')} {vacancy['salary']['currency']}"
    elif vacancy['salary']['from'] != None:
        vacancy['salary'] = f"{'{0:,}'.format(vacancy['salary']['from']).replace(',', ' ')} {vacancy['salary']['currency']}"
    elif vacancy['salary']['to'] != None:
        vacancy['salary'] = f"{'{0:,}'.format(vacancy['salary']['to']).replace(',', ' ')} {vacancy['salary']['currency']}"
    else:
        vacancy['salary'] = 'Нет данных'
    vacancy['key_skills'] = ', '.join(map(lambda x: x['name'], vacancy['key_skills']))
    return vacancy

def get_vacancies():
    try:
        params = {
            'text': 'game',
            'specialization': 1,
            'page': 1,
            'per_page': 100,
            'date_from': f'2022-12-21T00:00:00+0300',
            'date_to': f'2023-12-23T00:00:00+0300',
        }
        data = []
        info = requests.get('https://api.hh.ru/vacancies', params).json()
        print(info)
        for row in info['items']:
            data.append({'id': row['id'], 'published_at': row['published_at']})
        data = sorted(data, key=lambda x: x['published_at'])
        vacancies = []
        for vacancy in data[len(data) - 10:]:
            vacancies.append(clean_vacancy(requests.get(f'https://api.hh.ru/vacancies/{vacancy["id"]}').json()))
        return vacancies
    except Exception as e:
        print(e)
        print(datetime.datetime.now())
        return []


def main():
    get_vacancies()
    # data = []
    # info = requests.get('https://api.hh.ru/vacancies?text=%22devops%22&specialization=1&per_page=100').json()
    # # vacancies = get_page(1, '00:00:00', '23:59:59', '2023-01-05', 'devops')
    #
    # for row in info['items']:
    #     #print(f'    {row["published_at"]}---->{row["name"]}')
    #     if row['name'].lower().__contains__('devops') and not row['salary'] is None:
    #         data.append({'id': row['id'], 'published_at': row['published_at']})
    #         # data.append({'employer_name': row['employer']['name'], 'name': row['name'], 'salary_from': row['salary']['from'],
    #         #              'salary_to': row['salary']['to'],'key_skills':row['key_skills'],
    #         #              'salary_currency': row['salary']['currency'], 'area_name': row['area']['name'],
    #         #              'published_at': row['published_at']})
    # data = sorted(data, key=lambda x: x['published_at'], reverse=True)
    # print(data)
    # vacancies = []
    # for i, vacancy in enumerate(data):
    #     if i == 10:
    #         break
    #     #info = requests.get(f'https://api.hh.ru/vacancies/{vacancy["id"]}').json()
    #     # vacancies.append({'name': info['name'],
    #     #                   'description': info['description'],
    #     #                   'key_skills': info['key_skills'],
    #     #                   'employer': info['employer'],
    #     #                   'salary_from': info['salary']['from'],
    #     #                   'salary_to': info['salary']['to'],
    #     #                   'salary_currency': info['salary']['currency'],
    #     #                   'area_name': info['area']['name'],
    #     #                   'published_at': info['published_at']})
    #     vacancies.append(requests.get(f'https://api.hh.ru/vacancies/{vacancy["id"]}').json())
    # print(vacancies)



def crete_csv(name, date):
    """
    Создает csv файл по данным из hh.ru api
    Args:
        name(str): Имя файла
        date(str): дата для запроса
    :return:
    """
    print('\n' + date, end='')
    time.sleep(0.25)
    data = []
    text = 'devops'
    try:
        for page in range(0, 20):
            vacancies = get_page(page, '00:00:00', '23:59:59', date, text)
            if vacancies.__contains__('items'):
                if vacancies['found'] == 0:
                    break
                for row in vacancies['items']:
                    print(f'    {row["id"]}---->{row["name"]}')
                    if row['name'].lower().__contains__(text) and not row['salary'] is None:
                        data.append([row['id'], row['name'], row['salary']['from'], row['salary']['to'],
                                     row['salary']['currency'], row['area']['name'], row['published_at']])
            else:
                print(vacancies)  # для ошибок получении api запроса
            print(page)
    except Exception as e:
        print(e)
        return False
    if data:
        with open(f"{name}", "w", newline="", encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at'])
            writer.writerows(data)
    else:
        print(f'-----{data}----->clean')
    return True


def get_page(page, time_from, time_to, date, text):
    """
    Отправляет api запрос на hh.ru
    Arguments
        page: Номер страницы, с которой приходит вакансия (int)
        time_from: Начало временного промежутка, с которого начинается выбор вакансии (str)
        time_to: Конец временного промежутка, на котором заканчивается выбор вакансии (str)
        date: Дата, когда была опубликована вакансия (str)
    Returns:
        list: список вакансий в формате json
    """
    params = {
        'text': text,
        'specialization': 1,
        'page': page,
        'per_page': 100,
        'date_from': f'{date}T{time_from}+0300',
        'date_to': f'{date}T{time_to}+0300',
    }
    request = requests.get('https://api.hh.ru/vacancies', params).json()
    return request


if __name__ == '__main__':
    main()
