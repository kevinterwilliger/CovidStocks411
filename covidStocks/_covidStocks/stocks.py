import pymongo as pm
import statsmodels.tsa as tsa
import pprint
import pandas as pd
import numpy



def return_close(symbol):
    client = pm.MongoClient()

    observed = client.yfmongo.timeline.find({'ticker':symbol})

    dates = []
    close = []
    for point in observed:
        dates.append(point['date'])
        close.append(point['c'])
    return dates,close

def collect_tickers(company_symbols):
    # TODO: RETURN Dictionary of dataframes with predicted stocks
    # i.e data[Symbol]: Date Observed Model1 Model2 Model3 ...
    # symbols = dict()
    data = dict()
    dates = dict()
    for ticker in company_symbols:
        dates[ticker],data[ticker] = return_close(ticker)

    old = 0
    for d in dates:
        if old is 0:
            old = len(dates[d])
        else:
            if len(dates[d]) != old:
                raise Exception("Date lengths not equal")
    data['date'] = dates['PFE']
    return pd.DataFrame.from_dict(data).set_index('date')

def derive_models(data,sentiment):
    return data
