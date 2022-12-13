import pandas as pd
import csv
import os


def degree_to_fahrenheit(temperature: int) -> int or str:
    """Преобразует температуру в градусах Цельсия в градусы Фаренгейта
    Args:
        temperature (int): Значение температуры в Цельсиях
    Returns:
        int or str: Возвращаемое значение в Фаренгейтах , либо NaN
    """
    return (temperature * 9 / 5) + 32


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