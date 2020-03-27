import datetime
import pickle
import os
import json
import numpy as np

import pandas as pd


def main():
    df = read_data()
    count = split_weeks(df)
    extract_user_and_retweet_data(count)


def csv_writer(filtered_data, count):
    filename = os.path.join('DataSet', 'weeks', 'data-from-week-' + str(count) + '.pkl')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    filtered_data.to_pickle(filename)

def read_data():
    print('Reading data from SWM-dataset.csv...')
    data = pd.read_csv(os.path.join('DataSet', 'SWM-dataset.csv'))
    data['dates'] = pd.to_datetime(data['postedtime']).dt.date
    data['time'] = pd.to_datetime(data['postedtime']).dt.time

    df = pd.DataFrame(data,
                    columns=['tid', 'retweet_tid', 'screen_name_from', 'screen_name_to', 'postedtime', 'dates', 'time'])
    return df


def split_weeks(df):
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
    return count


def extract_user_and_retweet_data(count):
    print('Extracting users and retweet data by week...')
    for week in range(1, count + 1):
        # load data from pickle
        print('Extracting data for week', week)
        week_data = pd.read_pickle(os.path.join('DataSet', 'weeks', 'data-from-week-' + str(week) + '.pkl'))

        # extract users and retweets
        tids = set()
        user_data = {}
        for user in week_data['screen_name_from'].unique():
            user_data[user] = set()
            for i in week_data[week_data['screen_name_from'] == user].index:
                tid = week_data['retweet_tid'][i]
                user_data[user].add(tid)
                tids.add(tid)
            # filter out users with only 1 retweet
            if len(user_data[user]) == 1:
                del user_data[user]

        print("Number of users in week " + str(week) + ": " + str(len(user_data)))
        print("Number of tweets in week " + str(week) + ": " + str(len(tids)))

        # save result to pickle
        data_folder = os.path.join('DataSet', 'users')
        tweets_folder = os.path.join('DataSet', 'tweets')
        users_filename = 'data-from-week-' + str(week)
        tweets_filename = 'tweets-from-week-' + str(week)
        write_pickle(user_data, data_folder, users_filename)
        write_pickle(tids, tweets_folder, tweets_filename)

        week = week + 1
    print('Extraction complete')


def build_user_vectors(count):
    print("Building user retweet vectors by week...")
    for week in range(1, count + 1):
        # load data from pickles
        print("Building user vectors for week", week)
        user_data = pickle.load(os.path.join('DataSet', 'users', 'data-from-week-' + str(week) + '.pkl'))
        tweet_data = pickle.load(os.path.join('DataSet', 'tweets', 'tweets-from-week-' + str(week) + '.pkl'))
        tids = list(tweet_data)

        # build user vectors
        user_vectors = {user: [tid for tid in tids if tid in retweets] for user, retweets in user_data}

        # save results to pickle
        vector_folder = os.path.join('DataSet', 'vectors')
        vector_filename = 'user-vectors-for-week-' + str(week)
        write_json(user_vectors, vector_folder, vector_filename)
    print('User vectors complete')

def write_pickle(data, folder_path, base_filename):
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, base_filename + '.pkl'), 'wb') as handle:
        pickle.dump(data, handle)


"""Function to write data to json for debugging purposes."""
def write_json(data, folder_path, base_filename):
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, base_filename + '.json'), 'w') as handle:
        json.dump(data, handle, cls=NpEncoder, ensure_ascii=False, indent=4)


"""This class is for encoding numpy types to json."""
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, set):
            return list(obj)
        else:
            return super(NpEncoder, self).default(obj)


if __name__ == '__main__':
    main()
