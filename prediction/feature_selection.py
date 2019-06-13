import pandas as pd
import datetime
import requests

def create_features(df, label=None):
    """
    Creates time series features from datetime index
    """
    df['hour'] = df['date'].dt.hour
    df['dayofweek'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['dayofmonth'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.weekofyear

    X = df[['hour','dayofweek','quarter','month','year',
           'dayofyear','dayofmonth','weekofyear']]
    return X

def separate_data(date):
    if '-' in date:
        date = date.split('-')
        for i in range(len(date)):
            date[i] = pd.to_datetime(date[i], dayfirst=True)
        df = pd.date_range(date[0], date[1], freq='h' )
    else:
        df = pd.date_range(start=pd.to_datetime(date, dayfirst=True), periods=24, freq='h')
    return(pd.DataFrame(df, columns = ['date']))


def date_now(df):
    past = False
    current = ''
    for i in range(len(df.date)):
        if datetime.datetime.now() > df.date.iloc[i]:
            past = True
            current = df.date.iloc[i]
    begin = df.date.iloc[0]
    result = {'past':past,'begin':begin, 'current':current}
    return (result)

def Energy_Parcer():
    url = 'https://ua.energy/wp-admin/admin-ajax.php' # название сервера который присылает данные на сайт
    payload = { # параметры ответа
        "Host": "ua.energy",
        "Connection": "keep-alive",
        "Content-Length": '75',
        "Origin": "https://ua.energy",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "Referer": "https://ua.energy/diyalnist/dyspetcherska-informatsiya/dobovyj-grafik-vyrobnytstva-spozhyvannya-e-e/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "_ga=GA1.2.1756074011.1542635370; _gid=GA1.2.785433389.1542635370; _fbp=fb.1.1542635370134.1141896228; pll_language=uk"
    }

    headers = {}
    over = {'action':'get_data_oes', 'report_date': '27.11.2018', 'type':'consumption', 'rnd': '0.478195319721614'} # параметры запроса
    return requests.post(url, data=over, json=payload).json()


def actual_value(dct):
    data = pd.DataFrame(Energy_Parcer())
    data['date'] = pd.to_datetime(data['date'])

    return(list(data.value[(data.date >= dct['begin'])&(data.date <= dct['current'])]))

def add_sum(df):
    summ = pd.DataFrame(df.sum(), columns = ['СУММАРНОЕ ЗНАЧЕНИЕ']).T.round(2)
    if 'fact' not in df.columns:
        summ['fact'] = [None]
    summ['error'] = [None]
    return (summ)

def errors(df):
    df['error'] = 100*abs(df['fact'] - df['predict'])/df['fact']
    df['error'] = df['error'].round(2)
    return df
