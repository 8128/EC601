#!/usr/bin/env python
# coding=utf-8
# Copyright 2018 Tianyi Tang tty8128@bu.edu
import mysql.connector
import sys

class mySQLmod(object):

    # you have to use the commit function to implement all changes
    
    def __init__(self,passwd,host,user):
        self.passwd = passwd
        self.host = host
        self.user = user
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

    def insert_to_userinfo(self,time,user_name,twitter_name):
        sql = "INSERT INTO twitter.userInfo VALUES ('0','"+time+"','"+user_name+"','"+twitter_name+"')"
        self.dbcursor.execute(sql)

    def search_certain_user(self,name):
        sql = "Select * from userInfo where user_name='"+name+"'"
        self.dbcursor.execute(sql)
        for line in self.dbcursor:
            print(line)

    def search_certain_twittername(self,name):
        sql = "Select * from twitter where twitter_name='"+name+"'"
        self.dbcursor.execute(sql)
        for line in self.dbcursor:
            print(line)

    def search_certain_time(self,time):
        sql = "Select * from userInfo where time='"+time+"'"
        self.dbcursor.execute(sql)
        for line in self.dbcursor:
            print(line)    

    def commit_change(self):
        try:
            self.db.commit()
        except:
            self.db.rollback()
        
class mongoDBmod(object):

    def __init__(self):
        pass

        