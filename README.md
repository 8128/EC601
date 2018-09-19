# EC601
This repository is used for EC601 class

Copyright Tianyi Tang tty8128@bu.edu

LAST UPDATE DATE:  2018.9.19


Table of Contents
=================

   * [EC601](#ec601)
      * [Mini Project 1](#mini-project-1)
         * [Twitter.py](#twitterpy)
            * [get_all_tweets_pics(screen_name)](#get_all_tweets_picsscreen_name)
            * [pictureTag(numb)](#picturetagnumb)
            * [mpegvideo()](#mpegvideo)
            * [[deprecated]Upload_blob(bucket_name, source_file_name, destination_blob_name)](#deprecatedupload_blobbucket_name-source_file_name-destination_blob_name)
            * [[deprecated]analyze_explicit_content(path)](#deprecatedanalyze_explicit_contentpath)
         * [[deprecated]Analysis.py](#deprecatedanalysispy)



## Mini Project 1

This python file is used to download pictures from certain twitter user, change pictures to mpeg video and get tagged by Google Vision

### Twitter.py

Before you use this twitter.py, you have to apply for a twitter developer account. Enter your Twitter consumer, access key and secret in the head of this python file.

You also need to apply for a Google Account so you can use the Google cloud service. You need to set the following statement in your .bash_profile and restart your computer to ensure you can pass Google Authentication

```
export GOOGLE_APPLICATION_CREDENTIALS="YOUR AUTH JSON FILE PATH"
```

#### get_all_tweets_pics(screen_name)

- enter the twitter ID to download the pictures of him
- the picture names will be named as increasing number from 1.jpg
- the function will return you an int which shows the number of photos
- this function NEED twitter developer account

#### pictureTag(numb)

- enter the number of picture generated to tag them using Google Vision
- this step NEED Google Service, you have to pass the authentication
- the result will be written on left top pf the picture


#### mpegvideo()

- this function will generate the output mpeg video by pictures downloaded automatically
- the generated file name will be 'output.mp4'
- the frame rate is set to 0.25

#### [deprecated]Upload_blob(bucket_name, source_file_name, destination_blob_name)

- this function will allow you to upload blob file to Google Cloud
- google cloud account is needed, and you may be charged for this service

#### [deprecated]analyze_explicit_content(path)

- enter the GSU path of the video file you uploaded, this function can analyze explicit content of the video
- the result will be printed out

### [deprecated]Analysis.py

This python file provide a detailed review of the google cloud analysis function
