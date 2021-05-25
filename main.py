# This is a sample Python script.
from fredapi import Fred
import pandas as pd
import sklearn
import numpy as np
import time
fred = Fred(api_key='3c6ba58d26525f17af95af4fabed24be')
monthly_list = fred.search('monthly', limit=500, order_by='popularity', sort_order='desc',
                           filter=('frequency', 'Monthly'))
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
data = []
columns = []
o = 1
for i in monthly_list[["id"]].values:
    print(o)
    d = fred.get_series(i[0], observation_start="1/1/2000")
    columns.append(i[0])
    data.append(d)
    o += 1
    time.sleep(0.3)
data = pd.concat(data, axis=1)
data.columns = columns
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
print(data.head(-1))
data.to_csv("monthly_data.csv")
