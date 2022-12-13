import csv
import datetime
import os
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def degree_to_fahrenheit(temperature: int) -> int or str:
    """Преобразует температуру в градусах Цельсия в градусы Фаренгейта
    Args:
        temperature: Значение температуры в Цельсиях
    Returns:
        int or str: Возвращаемое значение в Фаренгейтах , либо NaN
    """
    return (temperature * 9 / 5) + 32


def str_transform_datetime(date: str) -> datetime.date:
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
df['temperature night'] = pd.to_numeric(
    df['temperature night'], errors='coerce')

# Добавление в конец значения температуры в Фаренгейтах

fahrenheit_day = []
fahrenheit_night = []

for i in range(len(df)):
    fahrenheit_day.append(degree_to_fahrenheit(df.iloc[i]['temperature day']))
    fahrenheit_night.append(degree_to_fahrenheit(df.iloc[i]['temperature night']))


df['fahrenheit temperature day'] = fahrenheit_day
df['fahrenheit temperature night'] = fahrenheit_night