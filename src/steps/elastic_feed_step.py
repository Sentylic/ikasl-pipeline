from step import _Step
from utils import call
from os import chdir, getcwd, listdir
from os.path import isfile, join
from shutil import copy


class ElasticFeedStep(_Step):
    param_names = ['dataset-name']

    def execute(self, in_dir):
        for f in listdir(in_dir):
            if isfile(join(in_dir, f)):
                out_json = f
                break

        visualizer_data_path = '../visualizer/Data/'
        copy(join(in_dir, out_json), visualizer_data_path)

        curr_dir = getcwd()
        chdir(visualizer_data_path)

        cmd0 = 'curl -XDELETE localhost:9200/{}'.format(
            self.params['dataset-name'])
        cmd1 = 'curl -XPUT localhost:9200/{}?pretty -H Content-Type:application/json'.format(
            self.params['dataset-name'])
        cmd2 = 'curl -XPOST http://localhost:9200/{}/_bulk?pretty -H "Content-Type:application/x-ndjson" --data-binary @{}'.format(
            self.params['dataset-name'], out_json)

        with open('curl-out-{}'.format(self.pipe_id), 'w') as out_f:
            call(cmd0)  # set stdout=out_f if wanted
            call(cmd1)  # set stdout=out_f if wanted
            call(cmd2, stdout=out_f)

        print '\nData fed to elastic server. Open http://localhost:3000/{}/graph.html'.format(
            self.params['dataset-name'])

        chdir(curr_dir)
        return in_dir


__all__ = ['ElasticFeedStep']
