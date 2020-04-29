import datetime
import pickle
import os
import json
import multiprocessing

import numpy as np
import pandas as pd
from collections import defaultdict


def main():
    df = read_data()
    count = split_weeks(df, 7)
    extract_user_and_retweet_data(count, 7)
    build_user_vectors(count, 7)


def csv_writer(filtered_data, count, timeperiod):
    filename = os.path.join('DataSet_{}_day'.format(timeperiod), 'weeks', 'data-from-week-' + str(count) + '.pkl')
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

def get_user_and_retweet_threshold(dataframe, botnames_set):
    users = set(dataframe["screen_name_from"].tolist())
    week_botnames = botnames_set.intersection(users)
    
    bot_tweets = dataframe[dataframe["screen_name_from"].isin(week_botnames)]
    bots_tweet_count = defaultdict(int)
    for idx,row in bot_tweets.iterrows():
        bots_tweet_count[row["screen_name_from"]] += 1
    
    
    if len(bot_tweets) == 0:
        return 1,1

    bots_tweet_count_list = [*bots_tweet_count.values()]
    bots_tweet_count_list.sort()
    #print(bots_tweet_count_list)
    bot_tweets_group = bot_tweets.groupby("retweet_tid")
    bot_retweet_size = bot_tweets.groupby("retweet_tid").size()
    bot_retweet_size_list = bot_retweet_size.tolist()
    bot_retweet_size_list.sort()
    bot_retweet_quartile = bot_retweet_size_list[len(bot_retweet_size_list)//3]
    return max(1, bot_retweet_quartile)
    
def split_weeks(df, timeperiod):
    print('Splitting the data by week and storing in pickle files...')
    count = 0
    from_date = df['dates'].min()
    
    botnames = pd.read_csv("botnames.csv")
    botnames_set = set(botnames["BotName"].tolist())
    while from_date <= df['dates'].max():
        to_date = from_date + datetime.timedelta(days=timeperiod)
        between_two_dates = (df['dates'] >= from_date) & (df['dates'] < to_date)
        filtered_data = df.loc[between_two_dates]
        
        retweet_threshold = get_user_and_retweet_threshold(filtered_data, botnames_set)
        #print(count, user_threshold, retweet_threshold)
        #Filter for removing single occurence retweets
        grouped_filtered_data = filtered_data.groupby("retweet_tid")
        filtered_rtids = [tid for tid, val in grouped_filtered_data if len(val) > 5]
        new_filtered_data = filtered_data[filtered_data.retweet_tid.isin(filtered_rtids)]

        if not new_filtered_data.empty:
            count = count + 1
            csv_writer(new_filtered_data, count, timeperiod)
        from_date = to_date
    print('Split complete, number of weeks:', count)
    return count


def extract_user_and_retweet_data(count, timeperiod):
    print('Extracting users and retweet data by week...')
    run_process_pool(extraction_worker, [(i, timeperiod) for i in range(1, count + 1)])
    print('Extraction complete')


def extraction_worker(week, timeperiod):
    # load data from pickle
    week_data = pd.read_pickle(os.path.join('DataSet_{}_day'.format(timeperiod), 'weeks', 'data-from-week-' + str(week) + '.pkl'))

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
        if len(user_data[user]) <= 4:
            del user_data[user]

    print("Number of users in week " + str(week) + ": " + str(len(user_data)))
    print("Number of tweets in week " + str(week) + ": " + str(len(tids)))

    # save result to pickle
    data_folder = os.path.join('DataSet_{}_day'.format(timeperiod), 'users')
    tweets_folder = os.path.join('DataSet_{}_day'.format(timeperiod), 'tweets')
    users_filename = 'data-from-week-' + str(week)
    tweets_filename = 'tweets-from-week-' + str(week)
    write_pickle(user_data, data_folder, users_filename)
    write_pickle(tids, tweets_folder, tweets_filename)


def build_user_vectors(count,timeperiod):
    print("Building user retweet vectors by week...")
    run_process_pool(vector_worker, [(i, timeperiod) for i in range(1, count + 1)])
    print('User vectors complete')


def vector_worker(week, timeperiod):
    # load data from pickles
    with open(os.path.join('DataSet_{}_day'.format(timeperiod), 'users', 'data-from-week-' + str(week) + '.pkl'), 'rb') as file:
        user_data = pickle.load(file)
    with open(os.path.join('DataSet_{}_day'.format(timeperiod), 'tweets', 'tweets-from-week-' + str(week) + '.pkl'), 'rb') as file:
        tweet_data = pickle.load(file)
    tids = list(tweet_data)

    # assign a bit position to each tweet in the week
    tid_bit_vectors = {tid: 1 for tid in tids}
    i = 1
    for tid in tid_bit_vectors.keys():
        tid_bit_vectors[tid] <<= i
        i += 1

    # build user vectors (the vectors are bit vectors to save space)
    user_vectors = {user: 1 for user in user_data.keys()}
    for user, retweets in user_data.items():
        for tid in retweets:
            user_vectors[user] |= tid_bit_vectors[tid]

    # save results to pickle
    vector_folder = os.path.join('DataSet_{}_day'.format(timeperiod), 'vectors')
    vector_filename = 'user-vectors-for-week-' + str(week)
    write_pickle(user_vectors, vector_folder, vector_filename)
    print("Completed vectors for week", week)


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


def run_process_pool(worker_func, args):
    pool = multiprocessing.Pool(abs(multiprocessing.cpu_count() - 2) or 1)
    pool.starmap(worker_func, args)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
