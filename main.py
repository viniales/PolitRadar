import praw
import os

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
user_agent = os.environ.get('user_agent')

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Subreddity do monitorowania
subreddits = ["Trump", "Biden"]

# Pobieranie postów z Redditu
posts = []
for subreddit_name in subreddits:
    new_posts = reddit.subreddit(subreddit_name).top(time_filter="day", limit=10)  # Pobierz 10 najpopularniejszych postów z ostatniego dnia
    for post in new_posts:
        posts.append(post)


# Wyświetlenie pobranych postów (do celów testowych)
for post in posts:
    with open('tekst.txt','a') as file:
        file.write(post.title+'\n')


