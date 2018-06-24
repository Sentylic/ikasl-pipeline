from step import _Step
from utils import get_sibling_dir
from layer_processor import process_layers


class LayerProcessStep(_Step):
    param_names = []

    def execute(self, in_dir):
        out_dir = self.get_out_dir(in_dir)
        
        # process_layers(7, )

        return out_dir

    def get_out_dir(self, in_dir):
        return get_sibling_dir(in_dir, 'layer-process-out')


__all__ = ['LayerProcessStep']
