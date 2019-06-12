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
    if request.method == "POST":
        date = request.POST.get("date")
#        if ':' in date:

        reg = pickle.load(open((settings.BASE_DIR + '/prediction/XGB.pkl'), 'rb'))
        df = feature_selection.separate_data(date)

        result = reg.predict(feature_selection.create_features(df))
        result = feature_selection.pd.DataFrame(result, columns =['predict'])
        result.index = df.date
        check_current = feature_selection.date_now(df)
        result['fact'] = [None for i in range(len(result['predict']))]
        result['error'] = [None for i in range(len(result['predict']))]
        result['predict']=result['predict'].astype(float).round(2)
        if check_current['past']:
            actual = feature_selection.actual_value(check_current)
            if len(actual) == len(result['predict']):
                result['fact'] = actual
                result['error'] = 100*abs(result['fact'] - result['predict'])/result['fact']
                result['error'] = result['error'].round(2)

                tag = '1'
                result[['fact','predict']].plot(figsize=(10,8), grid=True,style = ['g-','b-'],
                                                        linewidth=2,
                                                        title='Результат прогнозування').set_ylabel("МВт")
        else:
            result[['predict']].plot(figsize=(10,8), grid=True,style = ['g-'],
                                                    linewidth=2,
                                                    title='Результат прогнозування').set_ylabel("МВт")
            tag = '0'
        plt.savefig('static/figure.png')
    return render(request, 'home.html',
                    {"result":result, "tag":tag},)

def figure(request):
    return render(request, 'figure.html')
