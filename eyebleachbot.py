'''
Created on Dec 12, 2017

@author: Clarence
'''


import praw
from imgurpython import ImgurClient
from praw.models import Message
from praw.models import Comment
import random
import time
import sys

from _operator import contains
client_id = '*********'
client_secret = '*********'
client = ImgurClient(client_id, client_secret)
#items = client.gallery()
items = client.get_album('FlHzl')
#numPictures = items.__sizeof__()
reddit = praw.Reddit(client_id='*********',
                     client_secret="********", password='*********',
                     user_agent='eyebleachbot (by /u/su5)', username='eyebleachbot')

messageBod = '''User: {0}

Subject: {1}


Body: {2}'''
response = '''NSFL? Yikes!

[Eye Bleach!](%s)

I am a robit. '''
response2 = '''I think someone tagged this as NSFL! Yikes!

[Eye Bleach!](%s)

I am a robit. '''
complimentResponse = '''https://imgur.com/mkKd6Pi


I am a robit.'''
thanksResponse = '''[:)](https://imgur.com/Qdkw6T9)


I am a robit.'''
meanResponse = '''[Thank you for the feedback](https://imgur.com/deFLNvi)

I am a robit.
'''
repeatResponse = '''https://imgur.com/yJLpAwJ

I am a robit.
'''
viewPrint = 'Bleach views: {:d}, thanks: {:d}, compliemnts: {:d}, fuck yous: {:d}, total views: {:d}, Time Run: {:d}'
f = open('donestuff.txt','r')
lines = f.read().split(', ')
f.close()
fr = open('respond.txt','r')
resp = fr.read().split(', ')
fr.close() 
CommentsSubs = lines
respondedComs = resp
t0 = time.time()
print('starting')
t0 = time.time()
lastInbox = t0
lastView = t0
viewTimer = 120*60
inboxTimer = 15
unread_coms = []
count = 0
superCount = 0
numPictures = 0

def viewCount(t0):
    VCount = 0
    for pics in items.images:
        VCount = VCount+pics['views']
    thanksViews = client.get_image('Qdkw6T9').views
    complimentViews = client.get_image('mkKd6Pi').views
    fuckYouView = client.get_image('deFLNvi').views
    totalViews = VCount+thanksViews+complimentViews+fuckYouView
    #print("run time: {:d} hours".format( int( (time.time()-t0)/(60*60) ) ) )
    print(viewPrint.format(VCount,thanksViews ,complimentViews,fuckYouView,totalViews,int( (time.time()-t0)/(60*60) ) ) )
    
def giveThanks(reply):
    if reply.parent_id not in respondedComs:
        print("thanks found")      
        respondedComs.append(reply.parent_id)
        fr = open('respond.txt','a')
        fr.write(', ' + reply.parent_id)
        fr.close()
        reddit.comment(reply).reply(thanksResponse)  
        
def complimentRespond(reply):
    if reply.parent_id not in respondedComs:
        #print(reply.parent_id[3:])
        parent = reddit.comment(id = reply.parent_id[3:])
        if parent.body == complimentResponse:
            respondedComs.append(reply.parent_id)
            fr = open('respond.txt','a')
            fr.write(', ' + reply.parent_id)
            fr.close()
            reddit.comment(reply).reply(repeatResponse)
        elif parent.body == repeatResponse:
            print("super repeater!")
        else:
            print("Compliment found!")  
            respondedComs.append(reply.parent_id)
            fr = open('respond.txt','a')
            fr.write(', ' + reply.parent_id)
            fr.close()
            reddit.comment(reply).reply(complimentResponse)


def fuckYouRespond(reply):
    if reply.parent_id not in respondedComs:
        print("fuck you found")      
        respondedComs.append(reply.parent_id)
        fr = open('respond.txt','a')
        fr.write(', ' + reply.parent_id)
        fr.close()
        reddit.comment(reply).reply(meanResponse)        
        
def shutDownMessage(item):
    unread_messages.append(item)
    reddit.inbox.mark_read(unread_messages)
    print('SHUT IT DOWN')
    reddit.redditor(item.author).message('Shutting down!', "Shutting down!")
    sys.exit()
    
def healthCheckMessage(item):
    unread_messages.append(item)
    reddit.inbox.mark_read(unread_messages)
    reddit.redditor(str(item.author)).message('I am running', "I am running!")
    reddit.inbox.mark_read(unread_messages)
    print("health check!")

def getTotImages():
    numPictures = 0
    for pics in items.images:
        numPictures = numPictures+1
    return (numPictures -1) 




viewCount(t0)
numPictures = getTotImages()
while(True):
    try:
        for coms in reddit.subreddit('all').stream.comments():
            if coms.link_id not in CommentsSubs:
                if 'nsfl' in coms.body.lower():
                    if "http" in coms.body.lower():
                        items = client.get_album('FlHzl')
                        numPictures = getTotImages()
                        CommentsSubs.append(coms.link_id)
                        f = open('donestuff.txt','a')
                        f.write(', ' + coms.link_id)
                        f.close()
                        try:
                            reddit.comment(coms.id).reply(response % items.images[random.randint(1,numPictures)]['link'])
                        except Exception as e:  
                            print ("Had exception {0}, on comment {1}".format(str(e), coms.link_id) )
                        print(coms.permalink)
                    if coms.is_root == False:
                        prt = coms.parent()
                        if 'http' in prt.body.lower():
                            items = client.get_album('FlHzl')
                            numPictures = getTotImages()
                            print(coms.permalink)
                            CommentsSubs.append(coms.link_id)
                            CommentsSubs.append(prt.link_id)
                            f = open('donestuff.txt','a')
                            f.write(', ' + coms.link_id)
                            f.close()
                            try:
                                reddit.comment(prt.id).reply(response2 % items.images[random.randint(1,numPictures)]['link'])
                            except Exception as e:  
                                print (e) 
            if (time.time() - lastView) > viewTimer:
                viewCount(t0)
                lastView = time.time()
            if (time.time() - lastInbox)> inboxTimer:
                lastInbox = time.time()
                unread_messages = []
                for reply in reddit.inbox.unread():
                    #print(coms.link_id)
                    if isinstance(reply,Comment): 
                        if "good robit" in reply.body.lower() or "good bot" in reply.body.lower() or "good robot" in reply.body.lower() or "great bot"  in reply.body.lower() or "great robot" in reply.body.lower() or "great robit" in reply.body.lower():
                            complimentRespond(reply)
                        if "thank you" in reply.body.lower():
                            giveThanks(reply)
                        if "fuck you" in reply.body.lower():
                            fuckYouRespond(reply)
                    item = reply
                    if isinstance(item, Message):
                        if "health check" in item.body:
                            healthCheckMessage(item)
                        elif "shut down and stop" in item.body:
                            shutDownMessage(item)
                        else:
                            print("got a message")
                            reddit.redditor('su5').message('Eyebleachbot got a message!', messageBod.format(item.author, item.subject, item.body))
                        unread_messages.append(item)
                    reply.mark_read()
                reddit.inbox.mark_read(unread_messages)
                #print("finished with inbox")
    except Exception as e: 
        print("something DEEP went wrong! {0}".format(str(e)))
