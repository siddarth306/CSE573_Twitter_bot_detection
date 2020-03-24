import datetime
import pickle

import pandas as pd


def csv_writer(filtered_data, count):
    filtered_data.to_pickle('DataSet\\weeks\\data-from-week-' + str(count) + '.pkl')


data = pd.read_csv('DataSet\\SWM-dataset.csv')
data['dates'] = pd.to_datetime(data['postedtime']).dt.date
data['time'] = pd.to_datetime(data['postedtime']).dt.time

df = pd.DataFrame(data,
                  columns=['tid', 'retweet_tid', 'screen_name_from', 'screen_name_to', 'postedtime', 'dates', 'time'])

count = 1
from_date = df['dates'].min()
while from_date <= df['dates'].max():
    to_date = from_date + datetime.timedelta(days=7)
    between_two_dates = (df['dates'] >= from_date) & (df['dates'] < to_date)
    filtered_data = df.loc[between_two_dates]
    if not filtered_data.empty:
        csv_writer(filtered_data, count)
        count = count + 1
    from_date = to_date

week = 1
while week <= count:
    pickled_file = pd.read_pickle('DataSet\\weeks\\data-from-week-' + str(week) + '.pkl')
    d = {}
    for i in pickled_file['screen_name_from'].unique():
        d[i] = [{'retweet_tid': pickled_file['retweet_tid'][j],
                 'postedtime': pickled_file['postedtime'][j]}
                for j in pickled_file[pickled_file['screen_name_from'] == i].index]
        print(count)
        count = count + 1
    with open('DataSet\\users\\data-from-week-' + str(week) + '.pkl', 'wb') as handle:
        pickle.dump(d, handle)
    week = week + 1
