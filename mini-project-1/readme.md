# Table of Contents

[TOC]

## Mini Project 1

This python file is used to download pictures from certain twitter user, get tagged by Google Vision and changed pictures to mpeg video 

[2018-11-30 update] Now a database connector API is added.

This API is used for stroing user information and information of photos downloaded from twitter.

### minipj1.py

Before you use this twitter.py, you have to apply for a twitter developer account. Enter your Twitter consumer, access key and secret in the head of this python file.

You also need to apply for a Google Account so you can use the Google cloud service. You need to set the following statement in your .bash_profile and restart your computer to ensure you can pass Google Authentication

```shell
export GOOGLE_APPLICATION_CREDENTIALS="YOUR AUTH JSON FILE PATH"
```

You can choose to add

```python
os.system('export GOOGLE_APPLICATION_CREDENTIALS="YOUR AUTH JSON FILE PATH"')
```

to the main function, it is also correct

You NEED to install ffmpeg in your system before you start, the ffmpeg can be installed by brew

```shell
brew install ffmpeg
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

### db.py

#### Class mySQLmod

##### Prequisites 

- You have to download and install MySQL and start local service. You have to use Legacy Password Encryption or you may encounter connection problems.

- You have to install mysql-connector from python. Install by:

  ```bash
  pip install mysql-connector
  ```

- Make sure you do not have database named "twitter", although your database won't be wiped out, the function of db.py may not work well.

##### Initialization 

- To create the basic mySQLmod object, you have to provide your password, username. The host will be localhost if you do not enter.

#### Class mongoMod

##### Prerequisites

- You have to install pymongo first by

  ```bash
  pip install pymongo
  ```

- You have to set your mongodb up and start it using

  ```bash
  mongod
  ```