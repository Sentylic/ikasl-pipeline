from utils import *
import os
import datetime
from distutils.dir_util import copy_tree, remove_tree


class PipeLine():
    def __init__(self, out_dir='../out', out_sub_dir_name_equals_start_time=False, log_params_to_file=True):
        self.out_dir = os.path.abspath(out_dir)
        self.out_sub_dir_name_equals_start_time = out_sub_dir_name_equals_start_time
        self.steps = []
        self.bg_steps = []
        self.log_params_to_file = log_params_to_file
        self.pipe_id = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self._create_working_dir()

    def add_pipe(self, step):
        step.pipe_id = self.pipe_id
        self.steps.append(step)
        return self

    def add_bg_step(self, bg_step):
        bg_step.pipe_id = self.pipe_id
        self.bg_steps.append(bg_step)
        return self

    def run(self, in_dir):
        self.start_bg_processes()
        curr_dir = self._create_new_input_dir(in_dir)
        for step in self.steps:
            self._log_step_params(step)
            print pprint_message_str('Running {} with params {}'.format(
                step.__class__.__name__, str(step.params)))
            curr_dir = step.execute(curr_dir)
        self.finalize_bg_processes()
        return curr_dir

    def start_bg_processes(self):
        for bg_step in self.bg_steps:
            message = bg_step.run_bg()
            print pprint_message_str(message)

    def finalize_bg_processes(self):
        for bg_step in self.bg_steps:
            message = bg_step.finalize()
            print pprint_message_str(message)

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
            start_time = self.pipe_id
            self.working_dir = '{}/{}'.format(self.out_dir, start_time)
        else:
            self.working_dir = '{}/{}'.format(self.out_dir, 'pipe_out')
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)
