from bg_step import _BGStep
from utils import call_background, get_abs_path
import os
import psutil
import utils


class ElasticInitBGStep(_BGStep):
    param_names = ['kill_at_end']
    default_output_f = '../out/elastic_out'

    def run_bg(self, in_dir=None):
        if self.elastic_pid() == -1:
            if 'output_f' not in self.params:
                self.params['output_f'] = self.default_output_f
            if not os.path.exists(self.params['output_f']):
                os.makedirs(self.params['output_f'])
            self.output_f_name = '{}/stdout-{}'.format(
                self.params['output_f'], self.pipe_id)
            self.output_f = open(self.output_f_name, 'w')
            cmd_name = '../elasticsearch-5.0.2/bin/elasticsearch'
            call_background(cmd_name, stdout=self.output_f)
            return 'Elastic search initialized. The stdout is at {}'.format(
                self.output_f_name)
        else:
            return 'WARNING: Failed to initialize elasticsearch. elasticsearch is already running.'

    def finalize(self, in_dir=None):
        if hasattr(self, 'output_f'):
            self.output_f.close()
        if self.params['kill_at_end']:
            pid = self.elastic_pid()
            if pid > 0:
                psutil.Process(pid).terminate()
                if hasattr(self, 'output_f_name'):
                    return 'Elastic search terminated. The stdout is at {}'.format(
                        self.output_f_name)
                else:
                    return 'Elastic search terminated'
            else:
                return 'WARNING: Failed to kill elasticsearch. elasticsearch is not running.'

    def elastic_pid(self):
        for pid in psutil.pids():
            for cmd_param in psutil.Process(pid).cmdline():
                if 'org.elasticsearch.bootstrap.Elasticsearch' in cmd_param:
                    return pid
        return -1

    def validate_params(self):
        return self.params['kill_at_end'] in [True, False]

__all__ = ['ElasticInitBGStep']
