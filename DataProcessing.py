import datetime

import pandas as pd

data = pd.read_csv('DataSet\\SWM-dataset.csv')
data['dates'] = pd.to_datetime(data['postedtime']).dt.date
data['time'] = pd.to_datetime(data['postedtime']).dt.time
df = pd.DataFrame(data,
                  columns=['tid', 'retweet_tid', 'screen_name_from', 'screen_name_to', 'postedtime', 'dates', 'time'])


def csv_writer(filtered_data):
    from_date = str(filtered_data['dates'].min())
    to_date = str(filtered_data['dates'].max())
    filtered_data.to_csv(r'DataSet\\' + 'data-from-' + from_date + '-to-' + to_date + '.csv', index=False, header=True)


from_date = df['dates'].min()
while from_date <= df['dates'].max():
    to_date = from_date + datetime.timedelta(days=7)
    between_two_dates = (df['dates'] >= from_date) & (df['dates'] < to_date)
    filtered_data = df.loc[between_two_dates]
    if not filtered_data.empty:
        csv_writer(filtered_data)
    from_date = to_date
