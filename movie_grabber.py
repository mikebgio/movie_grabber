# CLI Tool for downloading Full Movies on YouTube via Reddit.
# See README.md for setup instructions
# V0.04 Adding in logging of posts and ability to pull
# new posts

import praw     # for interacting w/Reddit
import spinner  # bring in the loading animation

spin = spinner.Spinner()  # create a spinner from spinner.py
div = "\n" + ("~*" * 20)  # This is just a divider for printing
# Error msg for no guide comment
guide_error = "Sorry, there is no info available for this movie."

reddit = praw.Reddit('movie_grabber', user_agent='movie_grabber user agent')
subreddit = reddit.subreddit('fullmoviesonyoutube')


def get_submissions(subreddit, subs_viewed):
    """Grabs the 10 newest submissions"""
    print("Grabbing 10 movies...")
    # spin.start()  # animate spinner while running rest of method
    submissions = []   # This will be the list of 10 links, each stored as dict
    # Iterate through 10 newest submissions
    for submission in subreddit.new(limit=10):
        guide = get_guide_comment(submission)  # find MovieGuide comment
        if guide is None:  # if MovieGuide comment cannot be found, load error message
            guide = guide_error
        subdata = dict(  # Store submission data as dictionary of title:{necessary data}
            title=submission.title,
            subid=submission.id,
            link=submission.url,
            score=submission.score,
            guide=guide)  # store MovieGuide comment for user retrieval
        submissions.append(subdata)  # Store each submission dictionary in list
        log_viewed(submissions)
    # spin.stop()  # stop animation
    return submissions


def print_submissions(subslist):
    """Extracts titles from the submissions list and prints them
    out with index and score pretty-like"""
    for i, v in enumerate(subslist):
        print(str(i) + ": " + v['title'] +
              " :: SCORE: " + str(v['score']) + div)


def get_guide_comment(submission):
    """Checks the submission fed to it for a comment from MovieGuide.
    This comment bot provides a brief IMDB Blurb."""
    author = "MovieGuide"
    for comments in submission.comments:
        if comments.author == author:
            return comments.body


def print_more_info(query, subslist):
    """Provide user Title and Guide text if
    they enter <info-request-command>"""
    guide = subslist[query]['guide']  # load full guide comment source
    if guide == guide_error:
        description = guide
        cast_crew = ""
    else:
        cast_crew_start = guide.find("min]") + 6  # load start of the cast list
        cast_crew_end = cast_crew_start + \
            guide[cast_crew_start:].find("\n\n") + 4
        cast_crew = guide[cast_crew_start:cast_crew_end]
        description_start = guide.find('>')
        description_end = (description_start +
                           guide[description_start:].find('\nMore info'))
        description = guide[description_start:description_end]
    print(str(query) + ": " + subslist[query]['title'])
    print(cast_crew)
    print(description)


def log_viewed(submissions):
    """This will log submission.id for each post loaded
    so that the user can move on to more new posts"""
    with open('id_log.txt', 'w') as log:
        for i, v in enumerate(submissions):
            log.write(v['subid'] + '\n')


def view_log(submissions):
    with open('id_log.txt', 'r') as log:
        return log.read()

subs_viewed = []
subslist = get_submissions(subreddit, subs_viewed)
# print_submissions(subslist)
