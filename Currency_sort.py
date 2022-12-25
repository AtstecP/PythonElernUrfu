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
    min_date, max_date, dict_currency, dataframe = parser_csv(name)
    # print(dataframe)
    dict_currencies_new = {'date': None}
    for key in dict_currency.keys():
        if dict_currency[key] > 5000:
            dict_currencies_new[key] = dict_currency[key]
    dict_currencies_new.pop('')
    data_currency = create_csv(dict_currencies_new, min_date, max_date)
    print(data_currency)
    create_dataframe(dataframe, data_currency)


def create_dataframe(data, data_currency):
    """
    Записывает отформатированные данные в csv формат
        data(list): данные о вакансиях
        data_currency(dict): данные о курсах валют по года
    Returns:
         list: отформатированые данные
    """
    dataframe = [['name', 'salary', 'area_name', 'published_at']]
    flag = 0
    for row in data:
        if flag == 100:
            break
        flag += 1
        vacancy = [row[0]]
        try:
            cof = data_currency[row[5][:7]][row[3]]
        except Exception:
            cof = 1
        if cof == None:
            vacancy.append([None, row[5], row[4]])
            continue
        if row[1] == '' and row[2] != '':
            vacancy.append(round((float(row[2]) * cof), 1))
        elif row[1] != '' and row[2] == '':
            vacancy.append(round((float(row[1]) * cof), 1))
        elif row[1] != '' and row[2] != '':
            vacancy.append(round(((float(row[2]) + float(row[2])) * cof / 2), 1))
        else:
            vacancy.append(None)
        vacancy.append(row[4])
        vacancy.append(row[5])
        dataframe.append(vacancy)
    with open(f"F:/Makarov/3_3_2.csv", "w", newline="", encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(dataframe)
    return dataframe


def create_csv(dict_currencies_new, min_date, max_date):
    """
    Создает и записывает в csv файл данные по валютам с сайта ЦБ РФ,
    и возврашает их в виде словаря с датами в качестве ключей
    Args:
        dict_currencies_new(dict): словарь с валютами
        min_date(datetime): самая рання записаь
        max_date(datetime):  самая поздняя запись
    Returns:
        dict: данные о валютах по датам
    """
    data_currency = {}
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
            data_currency[dict_currencies_new['date']] = dict_currencies_new.copy()
            data_currency[dict_currencies_new['date']].pop('date')
            writer.writerow(dict_currencies_new.values())
    return data_currency


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
    dataframe = []
    with open(name, encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        heading = next(reader)
        for row in reader:
            dataframe.append(row)
            date = DataSet.format_time3(row[5])
            min_date = date if (date.timestamp() < min_date.timestamp()) else min_date
            max_date = date if (date.timestamp() > min_date.timestamp()) else max_date
            if dict_currencies.__contains__(row[3]):
                dict_currencies[row[3]] += 1
            else:
                dict_currencies[row[3]] = 0
    return min_date, max_date, dict_currencies, dataframe


if __name__ == "__main__":
    main()
