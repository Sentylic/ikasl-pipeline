
from pipeline import PipeLine
from steps import *

if __name__ == '__main__':
    pipeline = PipeLine()
    pipeline.add_bg_step(ElasticInitBGStep({'kill_at_end': False}))
    pipeline.add_bg_step(VisualizerInitBGStep({'kill_at_end': False}))
    pipeline.add_pipe(TweetBinStep(
        {
            'tweet-frequency': 'daily',
            'tweet-format': 'csv',
            'ignore-before': '2017-01-01'
        }))
    pipeline.add_pipe(FeatureExtractStep(
        {
            'jar-path': '../jars/TextFeatureExtractor.jar',
            'tweet-frequency': 'daily',
            'query-params': [
                'lka',
                'sri lanka', 'srilanka',
                'flag', 'celebration',
            ]
        }))
    pipeline.add_pipe(IKASLStep(
        {
            'jar-path': '../jars/IKASL.jar',
            'tweet-frequency': 'daily',
            'additional-args': {'htf': 0.02, '-max-nodes': 8}
        }))
    pipeline.add_pipe(LayerProcessStep({'tweet-frequency': 'daily'}))
    pipeline.add_pipe(ElasticFeedStep({'dataset-name': 'lka'}))
    # pipeline.run('../out/pipe_out/feature-extract-out')
    # pipeline.run('../out/pipe_out/ikasl-out')
    pipeline.run('../data/lka')
