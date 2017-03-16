# CLI Tool for downloading Full Movies on YouTube via Reddit.
# See README.md for setup instructions
# V0.03 App which gets links from r/fullmoviesonyoutube
# and now grabs MovieGuide comments for IMDb info

import praw     #for interacting w/Reddit
import spinner
#import config  #this will contain download options
#import time    #This will be used for request-limiting (maybe)
import os      #This will be used for storing history

spinney = spinner.Spinner() #create a spinner from spinner.py
div = "\n" + ("~*" * 20) # This is just a divider for printing
guide_error = "Sorry, there is no info available for this movie." # Error msg for no guide comment

reddit = praw.Reddit('movie_grabber', user_agent = 'movie_grabber user agent')
subreddit = reddit.subreddit('fullmoviesonyoutube')

def get_submissions(subreddit):
    """Grabs the 10 newest submissions"""
    print("Grabbing 10 movies...")
    spinney.start() #animate spinner while running rest of method
    submissions = []   # This will be the list of 10 links, each stored as dict
    for submission in subreddit.new(limit=10): # Iterate through 10 newest submissions
        guide = get_guide_comment(submission)
        if guide == None:
            guide = guide_error
        subdata = dict(title = submission.title, # Store submission data as dictionary of title:{necessary data}
            subid = submission.id,  
            link = submission.url,
            score = submission.score,
            guide = guide)
        submissions.append(subdata) # Store each submission dictionary in list
    spinney.stop() #stop animation
    return submissions

def print_submissions(subslist):
    """Extracts titles from the submissions list and prints them
    out with index and score pretty-like"""
    for i, v in enumerate(subslist):
        print(str(i) + ": " + v['title'] + " :: SCORE: " + str(v['score']) + div)

def get_guide_comment(submission):
    """Checks the submission fed to it for a comment from MovieGuide.
    This comment bot provides a brief IMDB Blurb."""
    author = "MovieGuide"
    for comments in submission.comments:
        if comments.author == author:
            return comments.body

def print_more_info(query, subslist):
    """Provide user Title and Guide text if they enter <info-request-command>"""
    guide = subslist[query]['guide'] #load full guide comment source
    if guide == guide_error:
        description = guide
        cast_crew = ""
    else:
        cast_crew_start = guide.find("min]") + 6 #load start of the cast list
        cast_crew_end = cast_crew_start + guide[cast_crew_start:].find("\n\n") + 4
        cast_crew = guide[cast_crew_start:cast_crew_end]
        description_start = guide.find('>')
        description_end = (description_start + guide[description_start:].find('\nMore info'))
        description = guide[description_start:description_end]
    print(str(query) + ": " + subslist[query]['title'])
    print(cast_crew)
    print(description) #Just prints RAW Source for now (will fix with string stuff)


subslist = get_submissions(subreddit)
print_submissions(subslist)