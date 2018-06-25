from pipe import *
from utils import *
import os
import datetime
from distutils.dir_util import copy_tree, remove_tree


class PipeLine():
    def __init__(self, out_dir='../out', out_sub_dir_name_equals_start_time=False, log_params_to_file=True):
        self.out_dir = os.path.abspath(out_dir)
        self.out_sub_dir_name_equals_start_time = out_sub_dir_name_equals_start_time
        self.steps = []
        self.log_params_to_file = log_params_to_file
        self._create_working_dir()

    def add(self, step):
        self.steps.append(step)
        return self

    def run(self, in_dir):
        curr_dir = self._create_new_input_dir(in_dir)
        for step in self.steps:
            self._log_step_params(step)
            print pprint_message_str('Running {} with params {}'.format(
                step.__class__.__name__, str(step.params)))
            curr_dir = step.execute(curr_dir)
        return curr_dir

    def _log_step_params(self, step):
        if self.log_params_to_file:
            with open('{}/param.log'.format(self.working_dir), 'a') as log_f:
                log_f.write(pprint_message_str(step.__class__.__name__) + '\n')
                for param_name, param in step.params.iteritems():
                    log_f.write('{}: {}'.format(param_name, param) + '\n')
                log_f.write('\n')

    def _create_new_input_dir(self, in_dir):
        in_dir_name = in_dir.split('/')[-1]
        copy_tree(in_dir, '../data/{}'.format(in_dir_name))
        in_dir = '../data/{}'.format(in_dir_name)
        new_in_dir = '{}/{}'.format(self.working_dir, in_dir_name)
        remove_tree(self.working_dir)
        if not os.path.exists(new_in_dir):
            os.makedirs(new_in_dir)
        copy_tree(in_dir, new_in_dir)
        return new_in_dir

    def _create_working_dir(self):
        if self.out_sub_dir_name_equals_start_time:
            start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M-%S')
            self.working_dir = '{}/{}'.format(self.out_dir, start_time)
        else:
            self.working_dir = '{}/{}'.format(self.out_dir, 'pipe_out')
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)


if __name__ == '__main__':
    pipeline = PipeLine()
    pipeline.add(TweetBinStep(
        {'tweet-frequency': 'daily', 'tweet-format': 'json'}))
    pipeline.add(FeatureExtractStep(
        {'jar-path': '../jars/TextFeatureExtractor.jar', 'tweet-frequency': 'daily', 'in-place': 'False', 'query-params': ["facebook", "delete", "fb", "deletefacebook"]}))
    pipeline.add(IKASLStep(
        {'jar-path': '../jars/IKASL.jar', 'in-place': 'False', 'tweet-frequency': 'daily', 'additional-args': {'htf': 0.0025}}))
    pipeline.add(LayerProcessStep({'tweet-frequency': 'daily'}))
    pipeline.run('../data/1')
    # pipeline.run(
    #     '/home/isura/Documents/FYP/pipeline/out/pipe_out/ikasl-out')
