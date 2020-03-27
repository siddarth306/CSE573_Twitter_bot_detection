import datetime
import pickle
import os

import pandas as pd


def csv_writer(filtered_data, count):
    filename = os.path.join('DataSet', 'weeks', 'data-from-week-' + str(count) + '.pkl')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    filtered_data.to_pickle(filename)

print('Reading data from SWM-dataset.csv...')
data = pd.read_csv(os.path.join('DataSet', 'SWM-dataset.csv'))
data['dates'] = pd.to_datetime(data['postedtime']).dt.date
data['time'] = pd.to_datetime(data['postedtime']).dt.time

df = pd.DataFrame(data,
                  columns=['tid', 'retweet_tid', 'screen_name_from', 'screen_name_to', 'postedtime', 'dates', 'time'])

print('Splitting the data by week and storing in pickle files...')
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
print('Split complete, number of weeks:', count)

print('Extracting users and retweet data by week...')
week = 1
while week <= count:
    print('Extracting data for week', week)
    pickled_file = pd.read_pickle(os.path.join('DataSet', 'weeks', 'data-from-week-' + str(week) + '.pkl'))
    d = {}
    for i in pickled_file['screen_name_from'].unique():
        d[i] = [{'retweet_tid': pickled_file['retweet_tid'][j],
                 'postedtime': pickled_file['postedtime'][j]}
                for j in pickled_file[pickled_file['screen_name_from'] == i].index]
        count = count + 1
    filename = os.path.join('DataSet', 'users', 'data-from-week-' + str(week) + '.pkl')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as handle:
        pickle.dump(d, handle)
    week = week + 1
print('Extraction complete')
