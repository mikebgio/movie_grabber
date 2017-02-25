# CLI Tool for downloading Full Movies on YouTube via Reddit.
# V0.01 App which gets links from r/fullmoviesonyoutube

import praw
#import config
import time
import os
div = "\n" + ("~*" * 20) # This is just a divider for printing

reddit = praw.Reddit('movie_grabber', user_agent = "Getting Movies") #
subreddit = reddit.subreddit('fullmoviesonyoutube')

def get_submissions(subreddit):
    """Grabs the 10 newest submissions"""
    submissions = []   # This will be the list of 10 links, each stored as dict
    for submission in subreddit.new(limit=10): # Iterate through 10 newest submissions
        subdata = dict(title = submission.title, # Store submission data as dictionary of title:{necessary data}
            subid = submission.id,  
            link = submission.url,
            score = submission.score)
        submissions.append(subdata) # Store each submission dictionary in list
    return submissions

def print_submissions(subslist):
    """Extracts titles from the submissions list and prints them
    out with index and score pretty-like"""
    for i, v in enumerate(subslist):
        print(str(i) + ": " + v['title'] + " :: SCORE: " + str(v['score']) + div)

subslist = get_submissions(subreddit)
print_submissions(subslist)
#print(subslist)

