import csv
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import numpy as np
from datetime import datetime, timedelta
from PrintOrCreate import DataSet

data_currencies = {}


def main():
    """
    Вызывает метод чтения, затем убирает лишнии валюты и вызывает метод записи
    """
    name = 'vacancies_dif_currencies.csv'
    min_date, max_date, dict_currency, dataframe = parser_csv(name)
    createCurrencies_csv(dict_currency, DataSet.format_time3(min_date), DataSet.format_time3(max_date))
    print(data_currencies)
    # create_dataframe(dataframe)


def get_salary(df_):
    """
    Получает строки из DataFrame и возврашает данные о зарплате
    Args:
        df_: данные о вакансии
    Returns:
         float or None: сумма зарплаты если достаточно данных
    """
    # try:
    #     cof = data_currency[df_[5][:7]][df_[3]]
    # except Exception:
    #     cof = 1
    # if cof == None:
    #     return None
    # elif df_[1] == '' and df_[2] != '':
    #     return round((float(df_[2]) * cof), 1)
    # elif df_[1] != '' and df_[2] == '':
    #     return round((float(df_[1]) * cof), 1)
    # elif df_[1] != '' and df_[2] != '':
    #     return round(((float(df_[2]) + float(df_[2])) * cof / 2), 1)
    # else:
    #     return None
    try:
        cof = data_currencies[df_.published_at[:7]][df_.salary_currency]
    except Exception:
        cof = 1
    if cof == None:
        return None
    elif df_.salary_from == '' and df_.salary_to != '':
        return round((float(df_.salary_to) * cof), 1)
    elif df_.salary_from != '' and df_.salary_to == '':
        return round((float(df_.salary_from) * cof), 1)
    elif df_.salary_from != '' and df_.salary_to != '':
        return round(((float(df_.salary_to) + float(df_.salary_to)) * cof / 2), 1)
    else:
        return None


def create_dataframe(data):
    """
    Записывает отформатированные данные в csv формат
        data(list): данные о вакансиях
        data_currency(dict): данные о курсах валют по года
    Returns:
         DataFrame: отформатированые данные
    """

    df = pd.DataFrame(
        data={'name': data.name, 'salary': data.apply(get_salary, axis=1), 'area_name': data.area_name,
              'published_at': data.published_at}, )
    # df = data.assign(prod_country_rank=lambda df_: get_salary(df_))
    df.to_csv('100vacancies.csv', index=False)
    return df


def createCurrencies_csv(dict_currencies_new, min_date, max_date):
    """
    Создает и записывает в csv файл данные по валютам с сайта ЦБ РФ,
    и возврашает их в виде словаря с датами в качестве ключей
    Args:
        dict_currencies_new(dict): словарь с валютами
        min_date(datetime): самая рання записаь
        max_date(datetime):  самая поздняя запись
    """
    global data_currencies
    with open(f"F:/Makarov/currency_api.csv", "w", newline="", encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(dict_currencies_new.keys())
        for date in pd.date_range(start=min_date.strftime('%Y-%m-%d'),
                                  end=(max_date + timedelta(days=30)).strftime('%Y-%m-%d'), freq='M'):
            info = make_request([date.strftime('%m'), date.year])
            for key in list(dict_currencies_new.keys()):
                try:
                    dict_currencies_new[key] = info[key]
                except Exception:
                    dict_currencies_new[key] = None
                dict_currencies_new['RUR'] = 1
                dict_currencies_new['date'] = date.strftime('%Y-%m')
            data_currencies[dict_currencies_new['date']] = dict_currencies_new.copy()
            data_currencies[dict_currencies_new['date']].pop('date')
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
        min_date(datetime): самая рання записаь
        max_date(datetime):  самая поздняя запись
        dict_currencies_new(dict): словарь с валютами
        DataFrame: даныне из файла
    """
    df = pd.read_csv(name, )
    df.published_at = df.published_at.astype('string')
    currencies = {'date': None}
    currencies.update(df.salary_currency.value_counts() \
                      .loc[lambda x: x > 5000] \
                      .to_dict())
    return min(df.published_at), max(df.published_at), currencies, df


if __name__ == "__main__":
    main()
