import json
import os
import configparser
import random
import sqlite3
import tweepy

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cfg = configparser.ConfigParser()
with open(os.path.join(__location__, 'cfg.ini'), encoding='utf-8') as f:
    cfg.read_file(f)

var = cfg['auth']

conn = sqlite3.connect(os.path.join(__location__, 'yellowjackets.db'))
cur = conn.cursor()

current_season = 2

def check_reset():
    try:
        cur.execute("SELECT count(*) FROM quotes WHERE is_sent='FALSE'")
        res = cur.fetchall()
        if res[0][0]==0:
            print("all sent!")
            cur.execute("UPDATE quotes SET is_sent='FALSE'")
            conn.commit()
    except:
        print("could not complete request")

def get_quote():
    try:
        cur.execute(f"SELECT id,quote FROM quotes WHERE is_sent='FALSE' AND season={current_season} ORDER BY RANDOM() LIMIT 1")
        rows = cur.fetchall()
        if len(rows) < 1:
        	cur.execute("SELECT id,quote FROM quotes WHERE is_sent='FALSE' ORDER BY RANDOM() LIMIT 1")
        	rows = cur.fetchall()
        return rows[0]
    except:
        print("could not retrieve quote!")

def update_sent(id):
    try:
        cur.execute("UPDATE quotes SET is_sent='TRUE' WHERE id=" + str(id))
        conn.commit()
    except:
        print("could not update is_sent!")

def send_tweet(message):
    try:
        client = tweepy.Client(var['bearer'], var['api_key'], var['api_key_secret'], var['access_token'],
                               var['access_token_secret'])
        client.create_tweet(text=message[1])
        update_sent(message[0])
    except:
        print("could not connect to twitter")

try:
    check_reset()
    newQuote = get_quote()
    send_tweet(newQuote)
except:
    print("something went wrong!")

cur.close()
