# ETL pipeline for countries data:
# - extract data from REST Countries API
# - transform nested JSON into data frame
# - load data into PostgreSQL (Docker)

import pandas as pd
import requests
from sqlalchemy import create_engine

url = 'https://restcountries.com/v3.1/all'

#максимальное количество запрашиваемых params: 10
params = {
    'fields': 'name,capital,population,flags,region,subregion,currencies,languages,area,timezones'
}

timeout = 5


#выполнение api запроса с проверкой на ошибки с сервера и ошибку формата данных
def extract_countries_data():
    try:
        response = requests.get(url=url, params=params, timeout=timeout)

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            raise ValueError('return unexpected format')
        return data

    except requests.exceptions.RequestException:
        return None

    except ValueError:
        return None


#форматируем полученные данные в список словарей, чтобы потом записать в датафрейм
def transform_countries_data(data):
    result = []

    #решил через .get(), так как привычка с алгоритмов + достаточно безопасно, если вдруг в данных что-то не так
    for country in data:

        #атрибуты, которые точно в одном экземпляре для каждой страны (даже регион)

        country_names = country.get('name', {})
        country_name = country_names.get('common')
        country_official_name = country_names.get('official')

        flags = country.get('flags', {})
        flag_desc = flags.get('alt')
        flag_png = flags.get('png')

        population = country.get('population')
        area = country.get('area')
        region = country.get('region')
        subregion = country.get('subregion')

        #атрибуты с, возможно, несколькими экземплярами
        capital_list = country.get('capital')
        if capital_list:
            capital_name = ', '.join(capital_list)  # есть страны с несколькими столицами
        else:
            capital_name = None

        timezones = country.get('timezones')
        if timezones:
            timezone = ', '.join(timezones)
        else:
            timezone = None

        languages = country.get('languages')
        if languages:
            language = ', '.join(languages.values())
        else:
            language = None

        #у валют динамические ключи(
        currencies = country.get('currencies')
        if currencies:
            currency_list = []
            for currency in currencies.values():
                currency_list.append(currency.get('name'))
            currency_name = ', '.join(currency_list)
        else:
            currency_name = None

        #записываем в словарь
        record = {
            'country_name': country_name,
            'country_official_name': country_official_name,
            'capital': capital_name,
            'region': region,
            'subregion': subregion,
            'flag_desc': flag_desc,
            'flag_png': flag_png,
            'population': population,
            'area': area,
            'language': language,
            'currency_name': currency_name,
            'timezones': timezone
        }
        result.append(record)
    return result


#подключение к базе postgresql
def load_countries_data(countries):
    engine = create_engine(
        "postgresql://aleksei:1905@localhost:5433/countries"
    )

    countries.to_sql("countries", engine, if_exists="replace", index=False)


def main():
    data = extract_countries_data()
    if data:
        countries = pd.DataFrame(transform_countries_data(data))
        load_countries_data(countries)

if __name__ == '__main__':
    main()
