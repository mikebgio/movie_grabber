# CLI Tool for downloading Full Movies on YouTube via Reddit.
# See README.md for setup instructions
# V0.05 Adding in downloading framework

from __future__ import unicode_literals
import youtube_dl
import praw     # for interacting w/Reddit
import spinner  # bring in the loading animation

SPIN = spinner.Spinner()  # create a spinner from spinner.py
DIV = "\n" + ("~*" * 20)  # This is just a Divider for printing
# Error msg for no guide comment
GUIDE_ERROR = "Sorry, there is no info available for this movie."
AFFIRMATIVE = ['y', 'Y']
NEGATIVE = ['n', 'N']

reddit = praw.Reddit('movie_grabber', user_agent='movie_grabber user agent')
subreddit = reddit.subreddit('fullmoviesonyoutube')


def get_submissions(subreddit, subs_viewed):
    """Grabs the 10 newest submissions"""
    print("Grabbing 10 movies...")
    SPIN.start()  # animate spinner while running rest of method
    submissions = []   # This will be the list of 10 links, each stored as dict
    # Iterate through 10 newest submissions
    for submission in subreddit.new(limit=10):
        guide = get_guide_comment(submission)  # find MovieGuide comment
        if guide is None:  # if MovieGuide comment cannot be found, load error message
            guide = GUIDE_ERROR
        subdata = dict(  # Store submission data as dictionary of title:{necessary data}
            title=submission.title,
            subid=submission.id,
            link=submission.url,
            score=submission.score,
            guide=guide)  # store MovieGuide comment for user retrieval
        submissions.append(subdata)  # Store each submission dictionary in list
        log_viewed(submissions)
    SPIN.stop()  # stop animation
    return submissions


def print_submissions(subslist):
    """Extracts titles from the submissions list and prints them
    out with index and score pretty-like"""
    for i, v in enumerate(subslist):
        print(str(i) + ": " + v['title'] +
              " :: SCORE: " + str(v['score']) + DIV)


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
    if guide == GUIDE_ERROR:
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


def download_video(subslist, query):
    if type(query) is list:
        for choice in query:
            print('DOWNLOADING {}'.format(choice))
    else:
        print('DOWNLOADING {}'.format(query))
    pass


def query_user(subslist):
    query = input('Please select a movie:\n')
    if 'dl' in query:
        download_video(subslist, int(query[3:].split(',')))
    elif 'quit' in query:
        exit('QUITTING')
    else:
        print_more_info(int(query), subslist)
        new_query = input('Would you like to download?  (Y/N):\n')
        if new_query in ['y', 'Y']:
            download_video(subslist, int(query))
        elif new_query in ['n', 'N']:
            print_submissions(subslist)
            query = input('Please select a movie:\n')
        else:
            print('invalid input')


def main():
    subs_viewed = []
    while True:
        subslist = get_submissions(subreddit, subs_viewed)
        print_submissions(subslist)
        query_user(subslist)


if __name__ == '__main__':
    main()
