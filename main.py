import praw
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
user_agent = os.environ.get('user_agent')

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

subreddits = ["Trump", "Biden"]

posts = []
for subreddit_name in subreddits:
    new_posts = reddit.subreddit(subreddit_name).top(time_filter="day", limit=100)
    for post in new_posts:
        posts.append(post)

spark = SparkSession.builder.appName('PolitRadar').getOrCreate()

spark_posts = spark.createDataFrame([(post.title, post.selftext) for post in posts], ['title', 'text'])
spark_posts = spark_posts.withColumn('text', concat(col('title'), lit(' '), col('text')))
spark_posts = spark_posts.withColumn('clear_text', lower(regexp_replace(col('text'),'[^a-zA-Z\\s]', '')))
spark_posts.show()
