import utils
import re


class ScrapedTweetCsvParser:
    def __init__(self, out_dir, input_file, tweet_frequency, ignore_before='1970-1-1'):
        self.out_dir = out_dir
        self.input_file = input_file
        self.tweet_frequency = tweet_frequency
        self.ignore_before = ignore_before

    def parse(self, group_by_1000s=False):
        with open(self.input_file, 'r') as input_f:
            tweets = input_f.readlines()
            created_dirs = set()
            for data in tweets:
                info = data.split('> ', 1)
                if len(info) == 1:
                    continue
                tweet = re.sub(r'<Emoji:(.*?)>', '', info[1][:-1])
                tweet = re.sub(
                    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet)
                date = utils.get_date_from_raw(info[0])
                if self._ignore_date(date):
                    out_dir = self._dir_name(date)
                    created_dirs.add(out_dir)
                    output_file = out_dir + '/all/tweets'
                    utils.create_file_if_not_exist(output_file)
                    with open(output_file, 'a') as output_f:
                        output_f.write(tweet + '\n')
            if group_by_1000s:
                utils.group_by_1000s(created_dirs)
            return created_dirs

    def _ignore_date(self, date):
        return utils.get_time_stamp(
            date, '%Y-%m-%d') > utils.get_time_stamp(self.ignore_before, '%Y-%m-%d')

    def _dir_name(self, date_str):
        return '{}/{}/{}'.format(self.out_dir, self.tweet_frequency.value, utils.get_dir_name(date_str, self.tweet_frequency))


if __name__ == '__main__':
    input_dir = '/home/isura/Documents/cricket-data'
    output_dir = '/home/isura/Documents/cricket-data'
    created_dirs = set()
    for input_file in utils.get_all_files_in_dir(input_dir):
        print 'Processing', input_file
        parser = ScrapedTweetCsvParser(
            output_dir, input_file, utils.TweetFrequency.daily)
        created_dirs.update(parser.parse())
    utils.group_by_1000s(created_dirs)
