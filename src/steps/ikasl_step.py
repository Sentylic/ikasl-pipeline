from step import _Step
from utils import get_sibling_dir, get_prev_dir, call
from distutils.dir_util import copy_tree
from os import chdir, getcwd


class IKASLStep(_Step):
    param_names = ['jar-path', 'additional-args', 'tweet-frequency']

    def execute(self, in_dir):
        out_dir = self.get_out_dir(in_dir)
        curr_dir = getcwd()
        chdir(get_prev_dir(self.params['jar-path']))

        feature_extract_command = 'java -cp {} com.algorithms.test.TestIKASL_TextDatabased_EventDetection_new_data -f {} -inp {} -outp {} {}'.format(
            self.params['jar-path'].split('/')[-1], self.params['tweet-frequency'], in_dir, out_dir, self.format_additional_args())
        call(feature_extract_command)

        chdir(curr_dir)
        return out_dir

    def validate_params(self):
        valid = self.params['tweet-frequency'] in ['daily', 'weekly', 'monthly']
        valid_addtional_arg_names = ['a', 'ansttrn', 'ansttst', 'dfunc', 'dmdt', 'f', 'fd', 'htf', 'it', 'mn', 'mnot', 'mnt', 'mxfunc', 'mxn', 'ns', 'nsi', 'nti', 'nwts', 'sf', 'tdt',
                                     '-alpha', '-aggregate-node-selection-threshold-training', '-aggregate-node-selection-threshold-testing', '-distance-func', '-doc-matching-distance-threshold', '-frequency', '-fd', '-hit-threshold-frac', '-init-type', '-merge-nodes', '-merge-nodes-overlap-threshold', '-merge-nodes-threshold', '-max-aggregation-func', '-max-nodes', '-neighborhood-size', '-no-smoothing-iter', '-no-training-iter', '-no-words-to-show', '-spread-factor', '-topic-discontinuity-threshold'
                                     ]
        for arg_name in self.params['additional-args']:
            valid = valid and arg_name in valid_addtional_arg_names
        return valid

    def get_out_dir(self, in_dir):
        return get_sibling_dir(in_dir, 'ikasl-out')

    def format_additional_args(self):
        return ' '.join([ \
                    '-{}'.format(arg_name) if arg_name in ['mn', 'merge-nodes'] else '-{} {}'.format(arg_name, arg_value)\
                        for arg_name, arg_value in self.params['additional-args'].iteritems() \
                    ])


__all__ = ['IKASLStep']
