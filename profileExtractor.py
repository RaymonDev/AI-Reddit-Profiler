
import praw
import datetime

#Reddit object
try:

    reddit = praw.Reddit(
        client_id="YOUR CLIENT ID",
        client_secret="YOUR CLIENT SECRET",
        user_agent="This is a test bot that gathers public information from subreddits and users on reddit.",
    )

except Exception as e:
    print("\033[91mError: ", e)
    
    
    
#Reddit object check
print("\033[94mRead only status: ", reddit.read_only, "\033[0m")
print("\033[92mReddit object created successfully\033[0m")


def getUserInfo(username: str):
    
    #Username without the u/
    redditorObj = reddit.redditor(username)
    karma = redditorObj.link_karma

    #Time of creation
    #Transform UTC to human readable time
    created_time = datetime.datetime.fromtimestamp(redditorObj.created_utc, datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')



    #Extract body and date of creatio of all the posts of the user
    postsText = []
    dateOfPostsCreation = []

    for submission in redditorObj.submissions.new(limit=None):
        postsText.append(submission.selftext)
        dateOfPostsCreation.append(datetime.datetime.fromtimestamp(submission.created_utc, datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))


    #Lists of subreddits the user is active in
    activeSubreddits = []
    for comment in redditorObj.comments.new(limit=None):
        activeSubreddits.append(comment.subreddit.display_name)


    return username, karma, created_time, postsText, dateOfPostsCreation, activeSubreddits




def infoFormatter(username:str, karma:int, created_time:str, postsText:list, dateOfPostsCreation:list, activeSubreddits:list):


    #Join each post text with its date of creation in one string
    posts = []
    for i in range(len(postsText)):
        posts.append(f"""
        - Post: {postsText[i]}
        - Date of creation: {dateOfPostsCreation[i]}
        """)
    posts = "\n".join(posts)





    final_str = f"""
    - Name: {username}
    - Karma: {karma}
    - Date of creation: {created_time}
    - Posts: {posts}
    - Active subreddits: {activeSubreddits}
    """
    return final_str














