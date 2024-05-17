import nltk
import praw
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from nltk.sentiment import SentimentIntensityAnalyzer
from pyspark.sql.types import FloatType

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
spark_posts = spark_posts.withColumn('clear_text', lower(regexp_replace(col('text'), '[^a-zA-Z\\s]', '')))

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    sentiment = sia.polarity_scores(text)
    return sentiment['compound']

sentiment_udf = udf(analyze_sentiment, FloatType())
spark_posts = spark_posts.withColumn("sentiment", sentiment_udf("clear_text"))

# Wyświetlenie wyników analizy sentymentu
spark_posts.select("clear_text", "sentiment").show()

# Zakończenie sesji Sparkclear
spark.stop()
