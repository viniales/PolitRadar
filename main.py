import praw
import os
from pyspark.sql import SparkSession

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
user_agent = os.environ.get('user_agent')

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

subreddits = ["Trump", "Biden"]

posts = []
for subreddit_name in subreddits:
    new_posts = reddit.subreddit(subreddit_name).top(time_filter="day", limit=10)
    for post in new_posts:
        posts.append(post)

spark = SparkSession.builder.appName('PolitRadar').getOrCreate()

spark_posts = spark.createDataFrame([(post.title, post.selftext) for post in posts], ["title", "text"])
spark_posts.show()
