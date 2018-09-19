# EC601
This repository is used for EC601 class

Copyright Tianyi Tang tty8128@bu.edu

LAST UPDATE DATE:  2018.9.18

[TOC]

## Mini Project 1

This python file is used to download pictures from certain twitter user, change pictures to mpeg video and get tagged by Google Vision

### Twitter.py

Before you use this twitter.py, you have to apply for a twitter developer account. Enter your Twitter consumer, access key and secret in the head of this python file.

You also need to apply for a Google Account so you can use the Google cloud service.  The Google developer JSON credentials is needed, you should enter it in the tail of the python file

#### get_all_tweets_pics(screen_name)

- enter the twitter ID you want to download the pictures of him
- the picture names will be named as increasing number from 1.jpg
- this function NEED twitter developer account

#### mpegvideo()

- this function will generate the output mpeg video by pictures downloaded automatically
- the generated file name will be output.mp4
- the frame rate is set to 0.25

#### Upload_blob(bucket_name, source_file_name, destination_blob_name)

- this function will allow you to upload blob file to Google Cloud
- google cloud account is needed, and you may be charged for this service

#### analyze_explicit_content(path)

- enter the GSU path of the video file you uploaded, this function can analyze explicit content of the video
- the result will be printed out

### Analysis.py

This python file provide a detailed review of the google cloud analysis function
