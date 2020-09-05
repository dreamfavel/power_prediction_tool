from django.shortcuts import render
from django.conf import settings

import pickle
from matplotlib import pyplot as plt

from . import feature_selection
# Create your views here.




def home(request):

    #date = '18.04.2018 12:00'
    result = ''
    tag = ''
    fig = ''
    summ = ''
    date = ''
    if request.method == "POST":
        tag = '0'

        date = request.POST.get("date")
#        if ':' in date:

        with open((settings.BASE_DIR + '/prediction/XGB.pkl'), 'rb') as f:
            reg = pickle.load(f)
        df = feature_selection.separate_data(date)

        result = reg.predict(feature_selection.create_features(df))
        result = feature_selection.pd.DataFrame(result, columns =['predict'])
        result.index = df.date
        check_current = feature_selection.date_now(df)
        result['fact'] = [None for i in range(len(result['predict']))]
        result['error'] = [None for i in range(len(result['predict']))]
        result['predict']=result['predict'].astype(float).round(2)
        summ = feature_selection.add_sum(result)

        if check_current['past']:
            actual = feature_selection.actual_value(check_current)
            if len(actual) == len(result['predict']):
                result['fact'] = actual
                tag = '1'
                if len(result['predict']) <= 24*7:
                    result[['fact','predict']].plot(figsize=(10,8), grid=True,style = ['g-','b-'],
                                                        linewidth=2,
                                                        title='Результат прогнозирования').set_ylabel("МВт")
                    fig = '1'
                summ = feature_selection.add_sum(result)
                print(summ)
                result = feature_selection.errors(result)
                summ = feature_selection.errors(summ)


        else:
            if len(result['predict']) <= 24*7:
                result[['predict']].plot(figsize=(10,8), grid=True,style = ['g-'],
                                                    linewidth=2,
                                                title='Результат прогнозирования').set_ylabel("МВт")
                fig = '1'


        plt.savefig('static/figure.png')
        result.append(summ).to_excel('static/result.xlsx')
        #feature_selection.pd.concat(lst).to_excel('result.xls')

    return render(request, 'home.html',
                    {"result":result, "summ":summ, "tag":tag, "fig":fig, "date":date },)

def figure(request):
    return render(request, 'figure.html',)
