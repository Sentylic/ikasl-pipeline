from step import _Step
from utils import get_sibling_dir
from layer_processor import process
from os import walk, path, makedirs
import json


class LayerProcessStep(_Step):
    param_names = ['tweet-frequency']

    def execute(self, in_dir):
        out_dir = self.get_out_dir(in_dir)
        if not path.exists(out_dir):
            makedirs(out_dir)
        in_dir_single_iter = '{}/{}_7'.format(in_dir,
                                              self.params['tweet-frequency'])
        time_stamps = self.get_time_stamps(in_dir_single_iter)
        process.process_layers(time_stamps, in_dir_single_iter, out_dir, self.pipe_id)
        return out_dir

    def get_out_dir(self, in_dir):
        return get_sibling_dir(in_dir, 'layer-process-out')

    def get_time_stamps(self, in_dir_single_iter):
        time_stamps = []
        for layer_fname in [path.join(in_dir_single_iter, fn) for fn in next(walk(in_dir_single_iter))[2]]:
            with open(layer_fname, 'r') as layer_f:
                time_stamp = json.load(layer_f)['label']
                time_stamps.append(time_stamp)
        return time_stamps

    def validate_params(self):
        return self.params['tweet-frequency'] in ['daily', 'weekly', 'monthly']


__all__ = ['LayerProcessStep']
