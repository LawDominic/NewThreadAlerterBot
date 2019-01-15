import praw
from urllib import request
import json
import requests
import mysql.connector
from bs4 import BeautifulSoup
from praw.models import Message

reddit = praw.Reddit('bot')

db = mysql.connector.connect(host="localhost",
                            port="3306",
                            user="root",
                            password="0000",
                            database="reddit")
                            
cursor = db.cursor(buffered=True)

def readInbox():

    for message in reddit.inbox.unread(limit=None):

        author = str(message.author).lower()
        body = str(message.body).lower()

        try:

            if message.subject.lower() == 'subscribe':
                subscribe_query = "INSERT INTO subscriptions(redditor,subreddit) VALUES (%s, %s)"

                try:
                    val = (author, body)
                    cursor.execute(subscribe_query, val)
                    db.commit()
                except Exception as e:
                    print(e)
                    print("Error has occured. - Select rows")
                finally:
                    db.close()
                    reddit.subreddit(message.body).subscribe()
                    message.reply('Subscribed.') 

            elif message.subject == "Unsubscribe" or message.subject == 'unsubscribe':
                unsubscribe_query = "DELETE FROM subscriptions WHERE redditor = %s AND subreddit = %s"

                try:
                    cursor.execute(unsubscribe_query, (author,body,))
                    db.commit()
                except Exception as e:
                    print(e)
                    print("Error has occured. - Unsubscribe")
                finally:
                    db.close()
                    reddit.subreddit(message.body).unsubscribe()
                    message.reply('Unsubscribed.') 

        except Exception as e:
            message.reply('An error has occured. If you continue to have this problem, please PM me with your issue.')

def emptyInbox():

    unread_messages = []
    for item in reddit.inbox.unread(limit=None):

        if isinstance(item, Message):
            unread_messages.append(item)

    reddit.inbox.mark_read(unread_messages)

def pullAndPushThreads():

    newThreads = list(reddit.front.new(limit=10))
    submissionList = []
    submissionID_query = "INSERT INTO submissionid(submissionID) VALUES (%s)"

    try:

        for item in newThreads:
            submissionList.append(item)
        for item in submissionList:
            output = str(item)
            val = (output,)
            cursor.execute(submissionID_query, val)

        cursor.execute("SELECT * FROM submissionid")
        newList = cursor.fetchall()
        id_list = []
        filter(newList, id_list)

        cursor.execute("SELECT * FROM oldsubmission")
        oldsubmission = cursor.fetchall()
        id_list1 = []
        filter(oldsubmission, id_list1)

        difference = set(id_list1).symmetric_difference(id_list)

        findRedditor_query = "SELECT redditor FROM subscriptions WHERE subreddit = %s"

        for item in difference:
            output = str(item)
        
            sub = str(reddit.submission(id=output).subreddit)

            subreddit = (sub, )
            cursor.execute(findRedditor_query, subreddit)

            rows = cursor.fetchall()
            id_list2 = []
            filter(rows, id_list2)

            for item in id_list2:
                redditor1 = str(item)
                print(redditor1)

            for message in reddit.inbox.sent(limit=15):
                dest = message.dest
                body = message.body
                link = "http://reddit.com/" + output
                
            if dest == redditor1 and body == link:
                pass
            else:
                reddit.redditor(redditor1).message('New post on ' + sub, '' + link)
            
    except Exception as e:
        print(e)
        print("Error has occured. - pullAndPushThreads")
    finally:
        cursor.execute("TRUNCATE oldsubmission")
        cursor.execute("INSERT INTO oldsubmission SELECT * FROM submissionid;")
        cursor.execute("TRUNCATE submissionid")
        cursor.close()
        db.commit()
        db.close()

def filter(list_, list_name):

    for index in range(len(list_)):
        list_name.append(list_[index][0])
        
    return list_name

if __name__ == "__main__":
    readInbox()
    emptyInbox()
    pullAndPushThreads()