# from command_callback import call

# parser_py_path = '/home/isura/Documents/FYP/IKASL-DataPreprocessor/parse.py'
# raw_data_set_path = '/home/isura/Documents/FYP/datasets/deletefacebook'
# raw_data_format = 'json'
# tweet_frequency = 'daily'

# feature_extract_jar_path = 'TextFeatureExtractor.jar'
# ikasl_jar_path = 'IKASL.jar'
# ikasl_additional_args = '-htf 0.02'
# ikasl_out_json = 'fb0_02.json'
# pathway_data_json = '/home/isura/Documents/FYP/pathway-visualizer/Data/fb0_02.json'
# name = 'fb0_02.json'

# preprocess_command = 'python {} -p {} -tfrq {} -tfmt {}'.format(parser_py_path, raw_data_set_path, tweet_frequency, raw_data_format)
# feature_extract_command = 'java -cp {} ExtractFeatures -f {} -p {}/'.format(feature_extract_jar_path, tweet_frequency, raw_data_set_path)
# ikasl_command = 'java -cp {} com.algorithms.test.TestIKASL_TextDatabased_EventDetection_new_data -p {}/ {}'.format(ikasl_jar_path, raw_data_set_path, ikasl_additional_args)
# proecess_layers_command = 'python process_layers.py > {}'.format(ikasl_out_json)
# curl_command_1 = 'curl -XPUT \'localhost: 9200/tweets?pretty\' -H \'Content-Type: application/json\''
# curl_command_2 = 'curl -XPOST \'http: // localhost: 9200/{}/_bulk?pretty\' -H "Content-Type:application/x-ndjson" --data-binary @{}'.format(name, pathway_data_json)

# print preprocess_command
# call([preprocess_command.split()], callback=lambda: \
#      call([feature_extract_command.split()], callback=lambda: \
#           call([ikasl_command.split()], callback=lambda: \
#                call([proecess_layers_command.split()], callback=lambda: \
#                     call([curl_command_1.split()], callback=lambda: \
#                         call([curl_command_2.split()], callback=lambda: ''))))))
