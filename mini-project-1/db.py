#!/usr/bin/env python
# coding=utf-8
# Copyright 2018 Tianyi Tang tty8128@bu.edu
import mysql.connector
import sys
from pymongo import MongoClient

class mySQLmod(object):

    # you have to use the commit function to implement all changes
    
    def __init__(self,passwd,user,host="localhost"):
        self.passwd = passwd
        self.host = host
        self.user = user
        self.log_insert = 0
        self.log_search = 0
        try:
            self.db = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database="twitter"
            )
            self.dbcursor = self.db.cursor()
            self.create_twitter_table()
        except:
            print("WRONG USER OR DB INFO. TRY TO CONNECT MYSQL...")
            try:
                self.db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd
                )
            except:
                print("WRONG HOSTNAME, USERNAME OR PASSWORD")
            else:
                print("NO TWITTER DATABASE. CREATE IT NOW...")
                self.create_twitter_db()
                print("TWITTER DB CREATED.")
                try:
                    self.db.connect(database="twitter")
                except:
                    print("CONNECT TO TWITTER DB FAILED")
        self.dbcursor = self.db.cursor()

    def create_twitter_db(self):
        try:
            self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd
            )
        except:
            print("WRONG DB INFO")
        self.dbcursor = self.db.cursor()
        self.dbcursor.execute("CREATE DATABASE IF NO twitter")
        self.create_twitter_table()

    def create_twitter_table(self):
        self.dbcursor.execute("create table if not exists twitter(id int(11) NOT NULL AUTO_INCREMENT,\
                                                            twitter_name TEXT,\
                                                            path  TEXT,\
                                                            label TEXT,\
                                                            primary key(id))")
        self.dbcursor.execute("create table if not exists userInfo(id int(11) NOT NULL auto_increment,\
                                                            time date,\
                                                            user_name varchar(50),\
                                                            twitter_name TEXT,\
                                                            primary key(id))")

    def list_db(self):
        self.dbcursor.execute("show databases")

    def list_tables(self):
        self.dbcursor.execute("show tables")

    def show_all_twitter_tables(self):
        self.dbcursor.execute("select * from twitter")
        for lines in self.dbcursor:
            print(lines)

    def show_all_userinfo_tables(self):
        self.dbcursor.execute("select * from userInfo")
        for lines in self.dbcursor:
            print(lines)

    def select_column_tables(self,table,column="*"):
        self.dbcursor.execute("select "+column+" from "+table)

    def insert_to_twitter(self,twitter_name,path,label):
        sql = "INSERT INTO twitter.twitter VALUES ('0','"+twitter_name+"','"+path+"','"+label+"')"
        self.dbcursor.execute(sql)
        self.log_insert+=1
        self.commit_change()

    def insert_to_userinfo(self,time,user_name,twitter_name):
        sql = "INSERT INTO twitter.userInfo VALUES ('0','"+time+"','"+user_name+"','"+twitter_name+"')"
        self.dbcursor.execute(sql)
        self.log_insert+=1
        self.commit_change()

    def search_certain_user(self,name):
        sql = "Select * from userInfo where user_name='"+name+"'"
        self.dbcursor.execute(sql)
        for line in self.dbcursor:
            print(line)
        self.log_search+=1

    def search_certain_twittername(self,name):
        sql = "Select * from twitter where twitter_name='"+name+"'"
        self.dbcursor.execute(sql)
        for line in self.dbcursor:
            print(line)
        self.log_search+=1

    def search_certain_time(self,time):
        sql = "Select * from userInfo where time='"+time+"'"
        self.dbcursor.execute(sql)
        for line in self.dbcursor:
            print(line)   
        self.log_search+=1 

    # this is a very important step, use this function every time or your data will not be stored
    def commit_change(self):
        try:
            self.db.commit()
        except:
            self.db.rollback()

    def close_connection(self):
        self.db.close()

    def report(self):
        print("DRUING THIS CONNECTION, YOU HAVE\n")
        print("INSERTED TO DATABASE "+str(self.log_insert)+" TIMES")
        print("SEARCHED IN DATABASE "+str(self.log_search)+" TIMES")


class mongoDBmod(object):

    def __init__(self,host='localhost',port=27017):
        self.host = host
        self.port = port
        self.client = MongoClient(self.host,self.port)
        db = self.client.twitter
        self.db_tw = db.twitter
        self.db_user = db.userInfo
        self.log_insert = 0
        self.log_search = 0

    def store_info_twitter(self, twitter_name, path, label):
        doc = {
            'twitter_id': twitter_name,
            'label': label,
            'path': path,
        }
        try:
            self.db_tw.insert_one(doc)
        except Exception as e:
            self.error = e
            raise e
        self.log_insert+=1

    def store_info_user(self, twitter_name, user, time):
        doc = {
            'twitter_id': twitter_name,
            'user_name': user,
            'date': time,
        }
        try:
            self.db_user.insert_one(doc)
        except Exception as e:
            self.error = e
            raise e
        self.log_insert+=1

    def search_user(self, key):
        user_list = []
        try:
            for col in self.db_user.find():
                if key in col['user_name']:
                    if col['user_name'] in user_list:
                        continue
                    else:
                        user_list.append(col['user_name'])
        except Exception as e:
            self.error = e
            raise e
        print (user_list)
        self.log_search+=1

    def search_twittername(self, key):
        try:
            result = self.db_tw.find({"twitter_id":key})
            for x in result:
                print(x)
        except:
            raise AttributeError
        self.log_search+=1

    def search_username(self, key):
        try:
            result = self.db_user.find({"user_name":key})
            for x in result:
                print(x)
        except:
            raise AttributeError
        self.log_search+=1

    def close_connection(self):
        self.client.close()

    def show_all_twitter(self):
        result = self.db_tw.find()
        for line in result:
            print(line)

    def show_all_user(self):
        result = self.db_user.find()
        for line in result:
            print(line)

    def report(self):
        print("DRUING THIS CONNECTION, YOU HAVE\n")
        print("ADDED INFO TO DATABASE "+str(self.log_insert)+" TIMES")
        print("SEARCHED IN DATABASE "+str(self.log_search)+" TIMES")