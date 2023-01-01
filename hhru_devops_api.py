import csv
import time

import pandas as pd
import requests

def main():
    for date in pd.date_range(start='2022-12-01', end='2022-12-31', freq='D'):
        crete_csv(f'devops_{date}.cvs', date)


def crete_csv(name, date):
    """
    Создает csv файл по данным из hh.ru api
    Args:
        name(str): Имя файла
        date(str): дата для запроса
    :return:
    """
    with open(f"{name}", "w", newline="", encoding='utf-8-sig') as f:
        for text in ['devops', 'development operations']:
            writer = csv.writer(f)
            writer.writerow(['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at'])
            for page in range(0, 20):
                vacancies = get_page(1, '00:00:00', '23:59:59', date, text)
                if vacancies.__contains__('items'):
                    for row in vacancies['items']:
                        if row['salary'] is None:
                            writer.writerow([row['name'], None, None, None, row['area']['name'], row['published_at']])
                        else:
                            writer.writerow([row['name'], row['salary']['from'], row['salary']['to'],
                                             row['salary']['currency'], row['area']['name'], row['published_at']])
                else:
                    print(vacancies)  # для ошибок получении api запроса
                time.sleep(0.25)


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
       # 'date_to': f'{date}T{time_to}+0300',
    }
    request = requests.get('https://api.hh.ru/vacancies', params).json()
    return request



if __name__ == '__main__':
    main()