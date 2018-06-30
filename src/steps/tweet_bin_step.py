from step import _Step
from tweet_categorizer import Parser
from utils import get_sibling_dir


class TweetBinStep(_Step):
    param_names = ['tweet-format', 'tweet-frequency']

    def execute(self, in_dir):
        if not 'ignore-before' in self.params:
            self.params['ignore-before'] = '1970-1-1'
        parser = Parser(
            self.params['tweet-format'], self.params['tweet-frequency'], in_dir, self.get_out_dir(in_dir), self.params['ignore-before'])
        parser.parse()
        return parser.out_dir

    def validate_params(self):
        return self.params['tweet-format'] in ['json', 'csv'] \
            and self.params['tweet-frequency'] in ['daily', 'weekly', 'monthly']

    def get_out_dir(self, in_dir):
        return get_sibling_dir(in_dir, 'tweet-bin-out')


__all__ = ['TweetBinStep']
