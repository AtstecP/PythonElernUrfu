import csv
import xml.etree.ElementTree as ET
import pandas as pd
import requests
from datetime import datetime, timedelta
from PrintOrCreate import DataSet


def main():
    """
    Вызывает метод чтения, затем убирает лишнии валюты и вызывает метод записи
    """
    name = 'vacancies_dif_currencies.csv'
    min_date, max_date, dict_currency = parser_csv(name)
    dict_currencies_new = {'date': None}
    for key in dict_currency.keys():
        if dict_currency[key] > 5000:
            dict_currencies_new[key] = dict_currency[key]
    dict_currencies_new.pop('')
    create_csv(dict_currencies_new, min_date, max_date)


def create_csv(dict_currencies_new, min_date, max_date):
    """
    Создает и записывает в csv файл данные по валютам с сайта ЦБ РФ
    Args:
        dict_currencies_new(dict): словарь с валютами
        min_date(datetime): самая рання записаь
        max_date(datetime):  самая поздняя запись
    """
    with open(f"F:/Makarov/currency_api.csv", "w", newline="", encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(dict_currencies_new.keys())
        for date in pd.date_range(start=min_date.strftime('%Y-%m-%d'),
                                  end=(max_date + timedelta(days=30)).strftime('%Y-%m-%d'), freq='M'):
            info = make_request([date.strftime('%m'), date.year])
            for key in dict_currencies_new.keys():
                try:
                    dict_currencies_new[key] = info[key]
                except Exception:
                    dict_currencies_new[key] = None
                dict_currencies_new['RUR'] = 1
                dict_currencies_new['date'] = date.strftime('%Y-%m')
            writer.writerow(dict_currencies_new.values())


def make_request(date):
    """
    Отправляет api запрос на www.cbr.ru
    Args:
        date(lis): месяц и год для api запроса
    Returns:
        dict: словарь с вакансиями и их ценой к рублю
    """
    response = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{date[0]}/{date[1]}')
    tree = ET.fromstring(response.content)
    currencies = {}
    for child in tree.findall('Valute'):
        currencies[child.find('CharCode').text] = float(child.find('Value').text.replace(',', '.')) / float(
            child.find('Nominal').text.replace(',', '.'))
    return currencies


def parser_csv(name):
    """
    Читате переданный csv файл
    Args:
        name(str): имя фала для считывания
    Returns:
        dict_currencies_new(dict): словарь с валютами
        min_date(datetime): самая рання записаь
        max_date(datetime):  самая поздняя запись
    """
    min_date = datetime.now()
    max_date = DataSet.format_time3('2000-07-14T11:06:59+0300')
    dict_currencies = {}
    with open(name, encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        heading = next(reader)
        for row in reader:
            date = DataSet.format_time3(row[5])
            min_date = date if (date.timestamp() < min_date.timestamp()) else min_date
            max_date = date if (date.timestamp() > min_date.timestamp()) else max_date
            if dict_currencies.__contains__(row[3]):
                dict_currencies[row[3]] += 1
            else:
                dict_currencies[row[3]] = 0
    return min_date, max_date, dict_currencies


if __name__ == "__main__":
    main()
