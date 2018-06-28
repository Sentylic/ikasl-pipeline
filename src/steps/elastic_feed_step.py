from step import _Step
from utils import call
from os import chdir, getcwd, listdir
from os.path import isfile, join
from shutil import copyfile


class ElasticFeedStep(_Step):
    param_names = ['tweets']

    def execute(self, in_dir):
        for f in listdir(in_dir):
            if isfile(join(in_dir, f)):
                out_json = f
                break

        visualizer_data_path = '../visualizer/Data'
        copyfile(out_json, visualizer_data_path)

        curr_dir = getcwd()
        chdir(visualizer_data_path)
        
        cmd1 = 'curl -XPUT \'localhost:9200/tweets?pretty\' -H \'Content-Type: application/json\''
        cmd2 = 'curl -XPOST \'http://localhost:9200/tweets/_bulk?pretty\' -H "Content-Type:application/x-ndjson" --data-binary @{}'.format(out_json)
        
        call(cmd1)
        call(cmd2)

        chdir(curr_dir)
        return in_dir
    
    def validate_params(self):
        pass
