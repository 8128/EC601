#!/usr/bin/env python
# encoding: utf-8
# Copyright Tianyi Tang 2018 tty8128@bu.edu


import tweepy
import subprocess
import os
import io
import db
import datetime

from PIL import Image
from PIL import ImageDraw
from urllib.request import urlretrieve
from google.cloud import vision
from google.cloud.vision import types

# Twitter API credentials
consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_key = "access_key"
access_secret = "access_secret"

class tweetApi(object):

    def __init__(self,screen_name,username):
        self.screen_name = screen_name
        self.username = username
        self.mysqlConnection = db.mySQLmod("your_password","your_username","your_host")
        self.mongoConnection = db.mongoDBmod()
        # write user info to database
        time_for_now = datetime.datetime.today().strftime('%Y-%m-%d')
        self.mysqlConnection.insert_to_userinfo(time_for_now,username,screen_name)
        self.mongoConnection.store_info_user(time_for_now,username,screen_name)

    # using twitter API to get all pics from certain username and return the number of picture
    def get_all_tweets_pics(self):
        # Twitter only allows access to a users most recent 3240 tweets with this method

        # authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        # initialize a list to hold all the tweepy Tweets
        alltweets = []

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=self.screen_name, count=10)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:

            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=self.screen_name, count=10, max_id=oldest)

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            if len(alltweets) > 15:
                break
            print
            "...%s tweets downloaded so far" % (len(alltweets))

        # download every pic in order
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

        self.picNum = picNum


    # using the ffmpeg to generate the mp4 from pictures with number
    def mpegvideo(self):
        ffmpeg_command = 'ffmpeg -framerate 0.25 -i %d.jpg output.mp4'
        # using os.system is also correct
        subprocess.call(ffmpeg_command, shell=True)


    # tag all the pictures using google vision API
    def pictureTag(self):
        # Instantiates a client
        client = vision.ImageAnnotatorClient()

        # The name of the image file to annotate
        path = os.getcwd()

        for i in range(1, self.picNum):
            file_name_jpg = path + "/" + str(i) + ".jpg"
            file_name = os.path.join(
                os.path.dirname(__file__),
                file_name_jpg)

            # Loads the image into memory
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations

            # openPic
            img = Image.open(file_name_jpg)

            # draw
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), str(labels), (255, 255, 255))  # Position/Content/Color

            # save
            img.save(str(i)+".jpg")

            # save to database
            self.mysqlConnection.insert_to_twitter(self.screen_name,str(i)+".jpg",str(labels))
            self.mongoConnection.store_info_twitter(self.screen_name,str(i)+".jpg",str(labels))


if __name__ == '__main__':
    m_api = tweetApi("@Ibra_official","a_user")
    m_api.get_all_tweets_pics()
    m_api.pictureTag()
    m_api.mpegvideo()
    m_api.mysqlConnection.show_all_twitter_tables()
    m_api.mysqlConnection.show_all_userinfo_tables()
