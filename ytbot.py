#!/usr/bin/python

import re, time, datetime
from apiclient.discovery import build
from apiclient.errors import HttpError
from db import Comments
import praw
from creds import *

# actually do stuff boolean
legit = True
log = True

# PRAW stuff
r = praw.Reddit('YouTube link/search bot by /u/MattCMultimedia')
r.login('ytbot', passwd)


# Youtube Data API v3 stuff
YT_DEV_KEY = key
SERVICE = "youtube"
VERSION = "v3"


c = re.compile("[.+]?/u/ytbot +?(?P<query>.+)\n?")

while True:
    recent_comments = r.get_comments("test")
    if log: print "Got Comments..."
    for comment in recent_comments:
        m = c.search(comment.body)
        if m:
            try:
                # this will raise exception if it doesn't exist
                exists = Comments.get(Comments.CommentID == comment.id)
            except:
                query = m.group('query')
                if log: print query

                # now grab the video from youtube with the most views for that search term
                try:
                    yt = build(SERVICE, VERSION, developerKey=YT_DEV_KEY)

                    response = yt.search().list(
                            q=query,
                            part="id,snippet",
                            maxResults=1
                        ).execute()

                    result = response.get("items", [])[0]
                    if log: print result

                    final_url = "http://www.youtube.com/watch?v=" + result['id']['videoId']
                    if log: print "-> " + final_url

                    if (legit):
                        comment.reply("Here's the top YouTube result!\n\n["+result['snippet']['title']+"]("+final_url+")\n\n ytbot created and maintained by /u/MattCMultimedia")
                        Comments.create(CommentID=comment.id, TSAdded=datetime.datetime.now())

                except HttpError, e:
                    if log: print e

    time.sleep(2)