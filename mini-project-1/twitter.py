#!/usr/bin/env python
# encoding: utf-8
# Copyright Tianyi Tang 2018 tty8128@bu.edu


import tweepy
from urllib.request import urlretrieve
import subprocess
import argparse
import os

from google.cloud import videointelligence

# Twitter API credentials
consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_key = "access_key"
access_secret = "access_secret"


def get_all_tweets_pics(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=10)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=10, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if len(alltweets) > 15:
            break
        print
        "...%s tweets downloaded so far" % (len(alltweets))

    picNum = 1

    for status in alltweets:
        entities = status._json.get('entities')
        media = entities.get('media', [{}])
        mediaDic = media[0]
        mediaURL = mediaDic.get('media_url', '')
        mediaName = str(picNum) + ".jpg"
        if mediaURL != '':
            URL = mediaURL
            urlretrieve(URL, mediaName)
            picNum += 1


def mpegvideo():
    # subprocess.call("ffmpeg -framerate 24 -i %d.jpg output.mp4", shell=True)
    ffmpeg_command = 'ffmpeg -framerate 0.25 -i %d.jpg output.mp4'
    subprocess.call(ffmpeg_command, shell=True)


def analyze_explicit_content(path):
    # [START video_analyze_explicit_content]
    """ Detects explicit content from the GCS path to a video. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.EXPLICIT_CONTENT_DETECTION]

    operation = video_client.annotate_video(path, features=features)
    print('\nProcessing video for explicit content annotations:')

    result = operation.result(timeout=90)
    print('\nFinished processing.')

    likely_string = ("Unknown", "Very unlikely", "Unlikely", "Possible",
                     "Likely", "Very likely")

    # first result is retrieved because a single video was processed
    for frame in result.annotation_results[0].explicit_annotation.frames:
        frame_time = frame.time_offset.seconds + frame.time_offset.nanos / 1e9
        print('Time: {}s'.format(frame_time))
        print('\tpornography: {}'.format(
            likely_string[frame.pornography_likelihood]))
    # [END video_analyze_explicit_content]


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets_pics("@Ibra_official")
    mpegvideo()
    os.system('export GOOGLE_APPLICATION_CREDENTIALS="Google credentials')
    analyze_explicit_content("path")
