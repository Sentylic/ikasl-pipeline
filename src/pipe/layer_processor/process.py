import numpy as np
import json
import random
import os
import time
import datetime


def process_layers(time_stamps, data_path, out_dir):
    emotions = ['sad', 'happy', 'angry', 'excited', 'fear']
    id2id = {}

    total_clusters = 0
    with open('{}/out.json'.format(out_dir), 'w') as out_f:
        for layer in xrange(len(time_stamps)):
            data = json.loads(open(data_path + "/layer_" + str(layer)).read())
            clusters = data['clusters']
            vocab = data['vocabulary']
            top_k = 10  # number of top words to show as the topic

            print '{} clusters: {}'.format(time_stamps[layer], len(clusters))
            total_clusters += len(clusters)

            for cluster in clusters:
                id = cluster['id']

                if id in id2id:
                    continue

                id2id[id] = len(id2id)
                id = id2id[id]
                if cluster['parentIDs'][0] == 'root':
                    parent_id = id
                else:
                    parent_id = id2id[cluster['parentIDs'][0]]

                hit_count = np.array(cluster['hitWordCount'])
                top_words = (np.negative(hit_count)).argsort()[:top_k + 1]
                topic = ""

                for word in top_words:
                    topic += vocab[word] + " "

                result = {}
                result['id'] = id
                result['parent'] = parent_id
                result['text'] = topic
                result['sentiment'] = random.randint(-2, 2)
                result['emotion'] = emotions[random.randint(0, len(emotions)-1)]
                result['time'] = time_stamps[layer]
                result['location'] = "dummy"
                result = json.dumps(result)

                other_json = {}
                index = {}
                index['_id'] = str(id)
                index['_type'] = 'tweet'
                other_json['index'] = index
                other_json = json.dumps(other_json)

                out_f.write(other_json + '\n')
                out_f.write(result + '\n')
        
    print 'total clusters:', total_clusters

# dataset = 'delete_facebook'
# #data_path = dataset + '/results/daily_9'
# raw_data_path = "/home/isura/Documents/FYP/datasets/deletefacebook/daily"

# # user should specify these accordingly
# layer_count = 7
# timestamps = []

# # get the timestamps
# #raw_data_path = 'datasets/' + dataset + '/daily'
# data_path = '/home/isura/Documents/FYP/datasets/deletefacebook/results/daily_7'

# for date in os.listdir(raw_data_path):
#     timestamps.append(int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())))

# emotions = ['sad', 'happy', 'angry', 'excited', 'fear']

# id2id = {}

# for layer in xrange(layer_count):
#     data = json.loads(open(data_path + "/layer_" + str(layer)).read())
#     clusters = data['clusters']
#     vocab = data['vocabulary']
#     top_k = 10 # number of top words to show as the topic

#     for cluster in clusters:
#         id = cluster['id']

#         if id in id2id:
#             continue

#         id2id[id] = len(id2id)
#         id = id2id[id]
#         if cluster['parentIDs'][0] == 'root':
#             parent_id = id
#         else:
#             parent_id = id2id[cluster['parentIDs'][0]]

#         hit_count = np.array(cluster['hitWordCount'])
#         top_words = (-hit_count).argsort()[:top_k + 1]
#         topic = ""

#         for word in top_words:
#             topic += vocab[word] + " "

#         result = {}
#         result['id'] = id
#         result['parent'] = parent_id
#         result['text'] = topic
#         result['sentiment'] = random.randint(-2, 2)
#         result['emotion'] = emotions[random.randint(0, len(emotions)-1)]
#         result['time'] = timestamps[layer]
#         result['location'] = "dummy"
#         result = json.dumps(result)

#         other_json = {}
#         index = {}
#         index['_id'] = str(id)
#         index['_type'] = 'tweet'
#         other_json['index'] = index
#         other_json = json.dumps(other_json)

#         print(other_json)
#         print(result)
