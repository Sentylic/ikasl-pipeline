
from pipeline import PipeLine
from steps import *

if __name__ == '__main__':
    pipeline = PipeLine()
    pipeline.add_bg_step(ElasticInitBGStep({'kill_at_end': False}))
    pipeline.add_bg_step(VisualizerInitBGStep({'kill_at_end': False}))
    # pipeline.add_pipe(TweetBinStep(
    #     {
    #         'tweet-frequency': 'daily',
    #         'tweet-format': 'json'
    #     }))
    # pipeline.add_pipe(FeatureExtractStep(
    #     {
    #         'jar-path': '../jars/TextFeatureExtractor.jar',
    #         'tweet-frequency': 'daily',
    #         'query-params': ["facebook", "delete", "fb", "deletefacebook"]}))
    # pipeline.add_pipe(IKASLStep(
    #     {
    #         'jar-path': '../jars/IKASL.jar',
    #         'tweet-frequency': 'daily',
    #         'additional-args': {'htf': 0.0025}
    #     }))
    pipeline.add_pipe(LayerProcessStep({'tweet-frequency': 'daily'}))
    pipeline.add_pipe(ElasticFeedStep({'dataset-name': 'fb'}))
    pipeline.run('../data/ikasl-out')
