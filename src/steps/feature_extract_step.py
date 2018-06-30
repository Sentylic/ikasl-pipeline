from step import _Step
from utils import get_sibling_dir, get_prev_dir, call
from distutils.dir_util import copy_tree
from os import chdir, getcwd


class FeatureExtractStep(_Step):
    param_names = ['jar-path', 'tweet-frequency', 'query-params']

    def execute(self, in_dir):
        out_dir = self.get_out_dir(in_dir)
        copy_tree(in_dir, out_dir)
        curr_dir = getcwd()
        chdir(get_prev_dir(self.params['jar-path']))

        self.params['query-params'] = [s.replace(' ', '@') for s in self.params['query-params']]
        feature_extract_command = 'java -cp {} ExtractFeatures -f {} -p {} -q {}'.format(
            self.params['jar-path'].split('/')[-1], self.params['tweet-frequency'], out_dir, ','.join(self.params['query-params']))
        call(feature_extract_command)

        chdir(curr_dir)
        return out_dir

    def validate_params(self):
        return self.params['tweet-frequency'] in ['daily', 'weekly', 'monthly']

    def get_out_dir(self, in_dir):
        return get_sibling_dir(in_dir, 'feature-extract-out')


__all__ = ['FeatureExtractStep']
