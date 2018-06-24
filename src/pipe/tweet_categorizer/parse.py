import argparse
import utils
from scraped_tweet_json_parser import ScrapedTweetJsonParser
from scraped_tweet_parser import ScrapedTweetParser

class Parser:
    def __init__(self, tweet_format, tweet_frequency, input_dir, out_dir):
        self.tweet_format = tweet_format
        self.tweet_frequency = utils.to_enum(tweet_frequency)
        self.input_dir = input_dir
        self.out_dir = out_dir

    def parse(self):
        if self.tweet_format == 'json':
            created_dirs = set()
            for input_file in utils.get_all_files_in_dir(self.input_dir):
                print 'Processing', input_file
                parser = ScrapedTweetJsonParser(self.out_dir, input_file, self.tweet_frequency)
                created_dirs.update(parser.parse())
            utils.group_by_1000s(created_dirs)
        elif self.tweet_format == 'csv':
            created_dirs = set()
            for input_file in utils.get_all_files_in_dir(self.input_dir):
                print 'Processing', input_file
                parser = ScrapedTweetParser(self.out_dir, input_file, self.tweet_frequency)
                created_dirs.update(parser.parse())
            utils.group_by_1000s(created_dirs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-tfmt', '--tweet_format',
                    choices=['json', 'csv'], help='format of the tweets', required=True)
    parser.add_argument('-p', '--dir_path',
                    help='path of the directory containing scraped tweets', required=True)
    parser.add_argument('-tfrq', '--tweet_frequency',
                    choices=['daily', 'weekly', 'monthly'], help='tweet occurring frequency', required=True)
    args = parser.parse_args()
    
    tweet_format = args.tweet_format
    input_dir = args.dir_path
    tweet_frequency = utils.to_enum(args.tweet_frequency)
    
    Parser(tweet_format, tweet_frequency, input_dir, input_dir).parse()
