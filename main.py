import praw
import os

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
user_agent = os.environ.get('user_agent')

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Subreddity do monitorowania
subreddits = ["Trump", "Biden", "election2024"]

# Pobieranie postów z Redditu
posts = []
for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    new_posts = subreddit.top(time_filter="day", limit=30)  # Pobierz 10 najpopularniejszych postów z ostatniego dnia
    for post in new_posts:
        posts.append(post)

count = 0
# Wyświetlenie pobranych postów (do celów testowych)
for post in posts:
    count += 1
    print(" ")
    print(post.title)

print(count)
