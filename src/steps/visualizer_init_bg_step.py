from bg_step import _BGStep
from utils import call_background, get_abs_path
import os
import psutil
import utils
import time


class VisualizerInitBGStep(_BGStep):
    param_names = ['kill_at_end']
    default_output_f = '../out/visualizer_out'

    def run_bg(self, in_dir=None):
        if self.visualizer_pid() == -1:
            if 'output_dir' not in self.params:
                self.params['output_dir'] = self.default_output_f
            if not os.path.exists(self.params['output_dir']):
                os.makedirs(self.params['output_dir'])
            self.output_f_name = '{}/stdout-{}'.format(
                self.params['output_dir'], self.pipe_id)
            self.output_f = open(self.output_f_name, 'w')
            self.initial_cwd = os.getcwd()
            os.chdir('../visualizer')
            cmd_name = 'node index.js'
            call_background(cmd_name, stdout=self.output_f)
            time.sleep(2)
            os.chdir(self.initial_cwd)
            return 'Visualizing server initialized. The stdout is at {}'.format(
                self.output_f_name)
        else:
            return 'WARNING: Failed to initialize visualizing server. Visualizing server is already running.'

    def finalize(self, in_dir=None):
        if hasattr(self, 'output_f'):
            self.output_f.close()
        if self.params['kill_at_end']:
            pid = self.visualizer_pid()
            if pid > 0:
                psutil.Process(pid).terminate()
                if hasattr(self, 'output_f_name'):
                    return 'Visualizing server terminated. The stdout is at {}'.format(
                        self.output_f_name)
                else:
                    return 'Visualizing server terminated.'
            else:
                return 'WARNING: Failed to kill visualizing server. Visualizing server is not running.'
        

    def visualizer_pid(self):
        for conn in psutil.net_connections():
            if (conn.laddr.ip == '::' or conn.laddr.ip == '127.0.0.1') and conn.laddr.port == 3000:
                for cmd in psutil.Process(conn.pid).cmdline():
                    if 'node' in cmd:
                        return conn.pid
        return -1

    def validate_params(self):
        return self.params['kill_at_end'] in [True, False]


__all__ = ['VisualizerInitBGStep']
