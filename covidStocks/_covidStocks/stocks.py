import pymongo as pm
import statsmodels.tsa as tsa
import statsmodels.tsa.stattools as st
from statsmodels.tsa import arima_model,arima,ar_model
from statsmodels.tsa.arima import model
import pprint
import pandas as pd
import numpy
import os



def return_close(symbol):
    client = pm.MongoClient()

    observed = client.yfmongo.timeline.find({'ticker':symbol})
    dates = []
    close = []
    for point in observed:
        dates.append(point['date'])
        close.append(point['c'])
    return pd.DataFrame.from_dict(dict(dates = pd.to_datetime(dates),
                                       close = close)).set_index('dates')

def collect_tickers(company_symbols):
    data = dict()
    for ticker in company_symbols:
        data[ticker] = return_close(ticker)
    return data
    # old = 0
    # for d in dates:
    #     if old is 0:
    #         old = len(dates[d])
    #     else:
    #         if len(dates[d]) != old:
    #             raise Exception("Date lengths not equal")
    # data['date'] = dates['PFE']
    # return pd.DataFrame.from_dict(data).set_index('date')

def derive_models(y,sentiment,symbol):
    models = y
    data = y['close']
    # sentiment = data/2
    max_iter = min(5,len(data)-1)
    best_ar = tsa.ar_model.ar_select_order(data,maxlag=max_iter,ic="aic")
    lags = 0 if best_ar.ar_lags is [] else 1
    max_lags = "AR(" + str(lags) + ")"
    ar_model = tsa.ar_model.AutoReg(data,lags=lags)
    # print(best_ar.fit().predict())
    models[max_lags] = ar_model.predict(ar_model.fit().params)

    best_ma_order = tsa.stattools.arma_order_select_ic(data, max_ar=0, max_ma=max_iter, ic="aic")
    min_order = "ARMA(0," + str(max(best_ma_order.aic_min_order)) + ")"
    # print(best_ma_order.aic_min_order)
    best_ma = tsa.arima.model.ARIMA(data,order=(0,0,best_ma_order.aic_min_order[1]))
    models[min_order] = best_ma.fit().predict()

    best_arma_model = st.arma_order_select_ic(data,max_ar=max_iter,max_ma=max_iter,ic="aic")
    arma_order = "ARMA(" + str(best_arma_model.aic_min_order) + ")"
    best_arma = tsa.arima.model.ARIMA(data,order=(best_arma_model.aic_min_order[0],0,best_arma_model.aic_min_order[1]))
    models[arma_order] = best_arma.fit().predict()

    best_arima = tsa.arima.model.ARIMA(endog=data,exog=sentiment,order=(best_arma_model.aic_min_order[0],0,best_arma_model.aic_min_order[1]))
    arima_order = "ARIMA(" + str(best_arma_model.aic_min_order) + "," + str(best_arima.fit().params[1]) + "*sentiment)"
    models[arima_order] = best_arima.fit().predict()
    return models

def write_predictions(company_symbols,sentiment):
    company_data = collect_tickers(company_symbols)
    dates = company_data['JNJ'].loc[company_data['JNJ'].index > "2020-10-31"].index
    for date in dates:
        if date not in sentiment.index:
            sentiment.loc[date] = [0 for sym in company_symbols]
    for sym in company_symbols:
        y = company_data[sym].loc[company_data[sym].index.isin(dates)].sort_index()
        sentiment = sentiment.loc[sentiment.index.isin(y.index)].sort_index()

        temp_data = derive_models(y=y,
                                  sentiment = sentiment[sym],
                                  symbol=sym)
        try:
            os.remove("csvFiles/"+sym+".csv")
        except:
            pass
        temp_data.to_csv("csvFiles/"+ sym +".csv")
    return True
