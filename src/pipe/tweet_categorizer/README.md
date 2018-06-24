##### Usage
```
usage: parse.py [-h] -tfmt {json,csv} -p DIR_PATH -tfrq {daily,weekly,monthly}

optional arguments:
  -h, --help            show this help message and exit
  -tfmt {json,csv}, --tweet_format {json,csv}
                        format of the tweets
  -p DIR_PATH, --dir_path DIR_PATH
                        path of the directory containing scraped tweets
  -tfrq {daily,weekly,monthly}, --tweet_frequency {daily,weekly,monthly}
                        tweet occurring frequency
```

##### Example

```
python parse.py -tfmt json -p /home/isura/Documents/FYP/datasets/deletefacebook -tfrq daily
```