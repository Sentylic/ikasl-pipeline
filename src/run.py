
from pipeline import PipeLine
from steps import *

if __name__ == '__main__':
    pipeline = PipeLine()
    pipeline.add_bg_step(ElasticInitBGStep({}))
    pipeline.add_pipe(TweetBinStep(
        {'tweet-frequency': 'daily', 'tweet-format': 'json'}))
    pipeline.add_pipe(FeatureExtractStep(
        {'jar-path': '../jars/TextFeatureExtractor.jar', 'tweet-frequency': 'daily', 'in-place': 'False', 'query-params': ["facebook", "delete", "fb", "deletefacebook"]}))
    pipeline.add_pipe(IKASLStep(
        {'jar-path': '../jars/IKASL.jar', 'in-place': 'False', 'tweet-frequency': 'daily', 'additional-args': {'htf': 0.0025}}))
    pipeline.add_pipe(LayerProcessStep({'tweet-frequency': 'daily'}))
    pipeline.run('../data/1')
    # pipeline.run(
    #     '/home/isura/Documents/FYP/pipeline/out/pipe_out/ikasl-out')
