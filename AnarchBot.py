'''
Created on Oct 28, 2013

@author: vostro
'''
'''
Created on Sep 4, 2013

@author: vostro
'''
import time
import re
import praw
posted = 0
posts = 20
done=[]

buildDone = True


subsToClone = [('anarchism','CommunityA',25)]

introComment = """Here is a link to the original submission


"""
additionalComment = """


*Here is a comment by the original submitter*


"""
shortenComment = """Had to shorten


"""
r = praw.Reddit(user_agent='AnBot')
print("logging in")
r.login()
print("logged in")
startTime = time.clock()



if buildDone:
    for a in subsToClone:
        placeToPost = a[1]
        submissions = r.get_subreddit(placeToPost).get_hot(limit = 2000)
        for s in submissions:
            done.append(s.url+placeToPost)
    timeEl = time.clock() - startTime
    print("That took %d seconds and we checked %d"%(timeEl,len(done)))

while True:
    try:
        for t in subsToClone:
            [subreddit,placeToPost,numPosts] = t
            try:
                hotGen = r.get_subreddit(subreddit).get_hot(limit=numPosts)
            except:
                print("failed to get posts from subreddit")
            for h in hotGen:
                id = str(h.url) + str(placeToPost)
                if id in done:
                    pass
                   # print("already did it")
                else:
                    title= str(h.title) + " " + " /u/" + str(h.author)
                    po=False
                    try:
                        
                        idd = r.submit(placeToPost, title, url=h.url)
                        print("posted",h.url)
                        po = True
                        posted+=1
                        done.append(h.url+placeToPost)
                        
                    except:
                        print("unable to submit",placeToPost)
                        try:
                            print(h.url)
                        except:
                            pass
                    if po: 
                        coms = h.comments
                        Comment = introComment + str(h.permalink)
                        for c in coms:
                            if type(c) is praw.objects.MoreComments:
                                print("lotta comments here...")
                            else:
                                if c.author == h.author: 
                                    Comment+=additionalComment + c.body
                        try:
                            idd.add_comment(Comment)
                        except:
                            print("Unable to comment")
                        
            hoursRun = (time.clock()-startTime)/60.0/60.0
            
            
    
        print("we have been running %.1f hours and posted %d things"%(hoursRun,posted))
        time.sleep(60*15)
    except:
        print('oops!')

                    










print("all done")
