import tweepy
from textblob import TextBlob
import credentials as cd
import pandas as pd
import re
import os
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import sys
import numpy as np
import nltk
from nltk.corpus import twitter_samples, stopwords


#clean text
def cleanText(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # Remove @mention
    text = re.sub(r'#', '', text)  # Removing the '#' symbol
    text = re.sub(r'RT[\s]+', '', text)  # Removing RT
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove the hyper link
    return text

def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
  return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    if score<0:
        return 'Negative'
    elif score==0:
        return 'Neutral'
    else:
        return 'Positive'




#getting credentials
consumerkey = cd.consumer_key
consumersecret = cd.consumer_secret
accessToken = cd.access_token
accessTokenSecret = cd.access_token_secret

#authentication dance
authenticate=tweepy.OAuthHandler(consumerkey, consumersecret)
authenticate.set_access_token(accessToken,accessTokenSecret)
api=tweepy.API(authenticate,wait_on_rate_limit=True)

#getting tweets
# keyword = input("Please enter keyword or hashtag to search:")
# noOfTweet = int(input ("Please enter how many tweets to analyze:"))
keyword = sys.argv[1]
noOfTweet = 200
tweets = tweepy.Cursor(api.search_tweets,q=keyword+"-filter:retweets",lang="en",tweet_mode="extended").items(noOfTweet)

#converted data into structure format

df=pd.DataFrame([tweet.full_text for tweet in tweets], columns=['Tweets'])
# print(df)
df['Tweets'] = df['Tweets'].apply(cleanText)

# df.drop_duplicates(subset='Tweets',keep='first',inplace=True)

df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)
df['Analysis'] = df['Polarity'].apply(getAnalysis)

# print(df)

ptweets = df[df.Analysis == 'Positive']
ptweets = str(ptweets['Tweets'])

ntweets = df[df.Analysis == 'Negative']
ntweets = ntweets['Tweets']

neutweets = df[df.Analysis == 'Neutral']
neutweets = neutweets['Tweets']

#data visulaization

#word cloud

desired_folder = "C:/Users/SURAJ BHATT/OneDrive/Desktop/django/hello/static/image/"
# os.makedirs(desired_folder)
name = "wplot.png"
full_path = os.path.join(desired_folder, name)

allWords = ' '.join([twts for twts in df['Tweets']])
wordCloud = WordCloud(width=500,height=300,random_state=21,max_font_size=119).generate(allWords)
plt.imshow(wordCloud,interpolation="bilinear")
plt.axis('off')
plt.savefig(full_path)
plt.show()

#bar graph

name2 = "bplot.png"
full_path2 = os.path.join(desired_folder, name2)

#df['Analysis'].value_counts()

plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind='bar',rot=0,figsize=(6,7))#width height
plt.savefig(full_path2)
plt.show()

#pie chart

p="piechart.png"
full_path3=os.path.join(desired_folder,p)

col=np.array(df['Analysis'].value_counts())
label=["positive","neutral","negative"]
plt.pie(col,labels=label)
plt.title("pie chart")
plt.savefig(full_path3)
plt.show()
