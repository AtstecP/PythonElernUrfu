import csv
import time
import requests


def main():
    crete_csv('hhru.csv', '2022-12-20')


def crete_csv(name, date):
    """
    Создает csv файл по данным из hh.ru api
    Args:
        name(str): Имя файла
        date(str): дата для запроса
    :return:
    """
    with open(f"F:/Makarov/{name}", "w", newline="", encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at'])
        for hour in range(0, 23):
            for page in range(0, 20):
                vacancies = get_page(page, f'{f"0{hour}" if hour < 10 else hour}:00:00',
                                     f'{f"0{hour + 1}" if hour + 1 < 10 else hour + 1}:00:00', date)
                if vacancies.__contains__('items'):
                    for row in vacancies['items']:
                        if row['salary'] is None:
                            writer.writerow([row['name'], None, None, None, row['area']['name'], row['published_at']])
                        else:
                            writer.writerow([row['name'], row['salary']['from'], row['salary']['to'],
                                             row['salary']['currency'], row['area']['name'], row['published_at']])
                else:
                    print(vacancies) # для ошибок получении api запроса
                time.sleep(0.25)


def get_page(page, time_from, time_to, date):
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
