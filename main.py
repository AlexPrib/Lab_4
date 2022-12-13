import csv
import datetime
import os
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def degree_fahrenheit(temperature: int) -> int or str:
    """Преобразует температуру в градусах Цельсия в градусы Фаренгейта
    Args:
        temperature: Значение температуры в Цельсиях
    Returns:
        int or str: Возвращаемое значение в Фаренгейтах , либо NaN
    """
    return (temperature * 9 / 5) + 32


def transform_datetime_str(date: str) -> datetime.date:
    """Делает из строки дату в формате datetime.date
    Args:
        date: Исходная дата
    Returns:
        datetime.date: Готовая дата
    """
    result = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:10]))
    return result



def sort_by_date_1(df: pd.DataFrame, first_date: datetime.date, second_date: datetime.date) -> pd.DataFrame:
    """Фильтрует DataFrame по двум датам , заданными в datetime.date
    Args:
        df: Исходный объект
        first_date: Первая дата
        second_date: Вторая дата
    Returns:
        pd.DataFrame: Отфильтрованный объект по двум датам
    """
    result = pd.DataFrame(columns=['date', 'temperature day', 'pressure',
                          'wind day', 'temperature night', 'pressure night', 'wind night', 'fahrenheit temperature day', 'fahrenheit temperature night'])
    flag = False

    for i in range(len(df)):

        if flag == False:

            if df.iloc[i]['date'] == pd.Timestamp(first_date.year, first_date.month, first_date.day):
                flag = True
                result.loc[len(result)] = [df.iloc[i]['date'], df.iloc[i]['temperature day'], df.iloc[i]['pressure day'], df.iloc[i]['wind day'], df.iloc[i]['temperature night'],
                                           df.iloc[i]['pressure night'], df.iloc[i]['wind night'], df.iloc[i]['fahrenheit temperature day'], df.iloc[i]['fahrenheit temperature night']]

        if flag:

            result.loc[len(result)] = [df.iloc[i]['date'], df.iloc[i]['temperature day'], df.iloc[i]['pressure day'], df.iloc[i]['wind day'], df.iloc[i]['temperature night'],
                                       df.iloc[i]['pressure night'], df.iloc[i]['wind night'], df.iloc[i]['fahrenheit temperature day'], df.iloc[i]['fahrenheit temperature night']]

            if df.iloc[i]['date'] == pd.Timestamp(second_date.year, second_date.month, second_date.day):
                break

    return result
    
def sort_by_date_2(df: pd.DataFrame, first_date: str, second_date: str) -> pd.DataFrame:
    """Фильтрует DataFrame по двум датам , заданными в str
    Args:
        df (pd.DataFrame): Исходный объект
        first_date (datetime.date): Первая дата
        second_date (datetime.date): Вторая дата
    Returns:
        pd.DataFrame: Отфильтрованный объект по двум датам
    """
    result = pd.DataFrame(columns=['date', 'temperature day', 'pressure day',
                          'wind day', 'temperature night', 'pressure night', 'wind night', 'fahrenheit temperature day', 'fahrenheit temperature night'])
    
    flag = False
    first_date = transform_datetime_str(first_date)
    second_date = transform_datetime_str(second_date)

    for i in range(len(df)):

        if flag == False:

            if df.iloc[i]['date'] == pd.Timestamp(first_date.year, first_date.month, first_date.day):
                flag = True
                result.loc[len(result)] = [df.iloc[i]['date'], df.iloc[i]['temperature day'], df.iloc[i]['pressure day'], df.iloc[i]['wind day'], df.iloc[i]['temperature night'],
                                           df.iloc[i]['pressure night'], df.iloc[i]['wind night'], df.iloc[i]['fahrenheit temperature day'], df.iloc[i]['fahrenheit temperature night']]

        if flag:

            result.loc[len(result)] = [df.iloc[i]['date'], df.iloc[i]['temperature day'], df.iloc[i]['pressure day'], df.iloc[i]['wind day'], df.iloc[i]['temperature night'],
                                       df.iloc[i]['pressure night'], df.iloc[i]['wind night'], df.iloc[i]['fahrenheit temperature day'], df.iloc[i]['fahrenheit temperature night']]

            if df.iloc[i]['date'] == pd.Timestamp(second_date.year, second_date.month, second_date.day):
                break

    return result



def sort_by_temp(df: pd.DataFrame, temperature: int) -> pd.DataFrame:
    """Функция фильтрует исходный объект DataFrame по температуре
    Args:
        df: Исходный объект
        temperature: Температура по которой фильтруется объект DataFrame
    Returns:
        pd.DataFrame: Возвращается отфильтрованный объект DataFrame
    """
    result = pd.DataFrame(columns=['date', 'temperature day', 'pressure day',
                          'wind day', 'temperature night', 'pressure night', 'wind night', 'fahrenheit temperature day', 'fahrenheit temperature night'])
    for i in range(len(df)):

        if df.iloc[i]['temperature day'] >= temperature:

            result.loc[len(result)] = [df.iloc[i]['date'], df.iloc[i]['temperature day'], df.iloc[i]['pressure day'], df.iloc[i]['wind day'], df.iloc[i]['temperature night'],
                                       df.iloc[i]['pressure night'], df.iloc[i]['wind night'], df.iloc[i]['fahrenheit temperature day'], df.iloc[i]['fahrenheit temperature night']]

    return result


def date_formatter(date: pd.Timestamp) -> str:
    """Форматирует дату согласно формату (год-месяц)
    Args:
        date: Дата
    Returns:
        str: Строка в определённом формате
    """

    year = date.year
    month = date.month

    if month < 10:
        month = '0' + str(month)

    else:
        month = str(month)

    return str(year) + '-' + month


def group_df(df: pd.DataFrame) -> pd.DataFrame:
    """Группирует DataFrame по месяцам и считает среднюю температуру
    Args:
        df: Исходный объект
    Returns:
        pd.DataFrame: Оформатированный объект
    """

    month = df.iloc[0]['date'].month
    dates_arr = []
    temp_month_arr = []

    output_date = []
    output_temp_d = []
    output_temp_n = []
    output_temp_f_d = []
    output_temp_f_n = []

    for i in range(len(df)):

        if df.iloc[i]['date'].month == month:
            temp_month_arr.append([df.iloc[i]['date'], df.iloc[i]['temperature day'], df.iloc[i]['temperature night'],
                                  df.iloc[i]['fahrenheit temperature day'], df.iloc[i]['fahrenheit temperature night']])
            if i == len(df) - 1:
                dates_arr.append(temp_month_arr)

        elif df.iloc[i]['date'].month != month:
            dates_arr.append(temp_month_arr)
            temp_month_arr = []
            if month == 12:
                month = 1
            elif month < 12:
                month += 1
            temp_month_arr.append([df.iloc[i]['date'], df.iloc[i]['temperature day'], df.iloc[i]['temperature night'],
                                  df.iloc[i]['fahrenheit temperature day'], df.iloc[i]['fahrenheit temperature night']])

    for montharr in dates_arr:

        t_d = np.array([])
        t_n = np.array([])
        f_t_n = np.array([])
        f_t_d = np.array([])

        for day in montharr:
            t_d = np.append(t_d, day[1])
            t_n = np.append(t_n, day[2])
            f_t_d = np.append(f_t_d, day[3])
            f_t_n = np.append(f_t_n, day[4])

        t_d = t_d[~np.isnan(t_d)]
        t_n = t_n[~np.isnan(t_n)]
        f_t_d = f_t_d[~np.isnan(f_t_d)]
        f_t_n = f_t_n[~np.isnan(f_t_n)]

        a = []
        b = []
        c = []
        d = []

        for i in range(len(t_d)):
            a.append(t_d[i])

        for i in range(len(t_n)):
            b.append(t_n[i])

        for i in range(len(f_t_d)):
            c.append(f_t_d[i])

        for i in range(len(f_t_n)):
            d.append(f_t_n[i])

        output_date.append(date_formatter(montharr[0][0]))
        output_temp_d.append(mean(a))
        output_temp_n.append(mean(b))
        output_temp_f_d.append(mean(c))
        output_temp_f_n.append(mean(d))

    result = pd.DataFrame({'date': output_date, 'avg. temperature day': output_temp_d, 'avg. temperature night': output_temp_n,
                          'avg. fahrenheit temperature day': output_temp_f_d, 'avg. fahrenheit temperature night': output_temp_f_n})

    return result


def draw_month_stat(df: pd.DataFrame, year: str or int, month: str or int) -> None:

    if type(month) == str:
        month = int(month)

    if type(year) == str:
        year = int(year)

    _date = []
    _temp_d = np.array([])
    _temp_n = np.array([])
    _temp_f_d = np.array([])
    _temp_f_n = np.array([])

    for i in range(len(df)):

        if df.iloc[i]['date'].month == month and df.iloc[i]['date'].year == year:
            _date.append(df.iloc[i]['date'])
            _temp_d = np.append(_temp_d, df.iloc[i]['temperature day'])
            _temp_n = np.append(_temp_n, df.iloc[i]['temperature night'])
            _temp_f_d = np.append(
                _temp_f_d, df.iloc[i]['fahrenheit temperature day'])
            _temp_f_n = np.append(
                _temp_f_n, df.iloc[i]['fahrenheit temperature night'])

        elif df.iloc[i]['date'].month == month + 1 and df.iloc[i]['date'].year == year:
            break

    table = pd.DataFrame({
        'date': _date,
        'temperature day': _temp_d,
        'temperature night': _temp_n,
        'fahrenheit temperature day': _temp_f_d,
        'fahrenheit temperature night': _temp_f_n
    })

    print(table)
    print('Медиана температуры дня в Цельсиях: ',
          table['temperature day'].median())
    print('Среднее значение температуры дня в указанный месяц: ',
          table['temperature day'].mean())

    t_c = plt.figure(figsize=(60, 5))
    plt.ylabel('Температура в Цельсиях')
    plt.xlabel('Месяца')
    plt.title('График изменения температуры за один месяц')
    plt.plot(table['date'], table['temperature day'], color='black',
             linestyle='-', marker='.', linewidth=1, markersize=4)
    plt.plot(table['date'], table['temperature night'], color='red',
             linestyle='-', marker='.', linewidth=1, markersize=4)
    plt.show()

    t_f = plt.figure(figsize=(60, 5))
    plt.ylabel('Температура в Фаренгейтах')
    plt.xlabel('Месяца')
    plt.title('График изменения температуры за один месяц')
    plt.plot(table['date'], table['fahrenheit temperature day'], color='black',
             linestyle='-', marker='.', linewidth=1, markersize=4)
    plt.plot(table['date'], table['fahrenheit temperature night'],
             color='red', linestyle='-', marker='.', linewidth=1, markersize=4)
    plt.show()


path = 'dataset.csv'

with open(path, 'r', encoding='utf-8') as file:
    data = list(csv.reader(file, delimiter=","))

    dates = []
    temperature_day = []
    pr_day = []
    wind_day = []
    temperature_night = []
    pr_night = []
    wind_night = []

    for i in data:

        dates.append(i[0])
        temperature_day.append(i[1])
        pr_day.append(i[2])
        wind_day.append(i[3])
        temperature_night.append(i[4])
        pr_night.append(i[5])
        wind_night.append(i[6])


# DataFrame

df = pd.DataFrame({
    'date': dates,
    'temperature day': temperature_day,
    'pressure day': pr_day,
    'wind day': wind_day,
    'temperature night': temperature_night,
    'pressure night': pr_night,
    'wind night': wind_night
})

df['date'] = pd.to_datetime(df['date'])

# обработка пропущенных значений

df['temperature day'] = pd.to_numeric(df['temperature day'], errors='coerce')
df['temperature night'] = pd.to_numeric(df['temperature night'], errors='coerce')

# Добавление в конец значения температуры в Фаренгейтах

fahrenheit_day = []
fahrenheit_night = []

for i in range(len(df)):
    fahrenheit_day.append(degree_fahrenheit(df.iloc[i]['temperature day']))
    fahrenheit_night.append(degree_fahrenheit(df.iloc[i]['temperature night']))


df['fahrenheit temperature day'] = fahrenheit_day
df['fahrenheit temperature night'] = fahrenheit_night

year = '2015'
month = '1'

draw_month_stat(df, year, month)