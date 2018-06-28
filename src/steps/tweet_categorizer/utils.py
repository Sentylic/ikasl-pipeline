import os
from enum import Enum
from os.path import isfile, join
from datetime import datetime, timedelta

def create_file_if_not_exist(file):
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))

def get_all_files_in_dir(dir):
    return [join(dir, path) for path in os.listdir(dir) if isfile(join(dir, path))]

def get_date_from_raw(raw):
    return raw.split(' ', 2)[1]

def group_by_1000s(created_dirs):
    for created_dir in created_dirs:
        with open(created_dir + '/all/tweets', 'r') as tweet_file:
            tweets = tweet_file.readlines()
            n = len(tweets)
            for i in range(0, n, 1000):
                chunk = tweets[i: min(i + 1000, n)]
                output_file = created_dir + '/' + str(i / 1000) + '/tweets'
                create_file_if_not_exist(output_file)
                with open(output_file, 'w') as output_f:
                    output_f.writelines(chunk)

def get_week(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    start = dt - timedelta(days=dt.weekday())
    return start.strftime('%Y-%m-%d')

def get_month(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    start = dt.replace(day=1)
    return start.strftime('%Y-%m-%d')

class TweetFrequency(Enum):
    daily='daily'
    weekly='weekly'
    monthly='monthly'

def get_dir_name(date_str, tweet_frequency):
    if tweet_frequency == TweetFrequency.daily:
        return date_str
    elif tweet_frequency == TweetFrequency.weekly:
        return get_week(date_str)
    elif tweet_frequency == TweetFrequency.monthly:
        return get_month(date_str)
    else:
        return None

def to_enum(tweet_frequency_str):
    if tweet_frequency_str == 'daily':
        return TweetFrequency.daily
    elif tweet_frequency_str == 'weekly':
        return TweetFrequency.weekly
    elif tweet_frequency_str == 'monthly':
        return TweetFrequency.monthly
    else:
        return None
