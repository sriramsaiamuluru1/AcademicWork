#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 22:04:20 2017

@author: sameerkumar
"""
"""
References:
http://stackoverflow.com/questions/9942594/unicodeencodeerror-ascii-codec-cant-encode-character-u-xa0-in-position-20
https://www.dropbox.com/sh/cpkokzf1ko0p53t/AAB4a6w6bO54iGC-7AgPzhh-a/JG_Ch20_Text_Mining/0_notebooks/text_part1_nltk_textblob_wordcloud_section001.ipynb?dl=0
"""
#Import all the necessary Packages. 
from wordcloud import WordCloud
from nltk.stem.snowball import SnowballStemmer
#Instantiate snowball stemmer
ss = SnowballStemmer("english") 
import matplotlib.pyplot as plt
import nltk
import json 

#Get the stop words from NLTK
stopwords = nltk.corpus.stopwords.words('english')
#Create an empty word list, will be used later. 
wordLst = []
#Counter variable to track the number of tweets processed. 
tweetsProcessed = 0
#Initial text with an empty string to be used later
text = ''
#Read the JSON file and load the tweets
with open("tweet_stream_trump_US_10000.json") as f:
    tweets = json.load(f)
#with open("tweet_stream_trump_TX_1000.json") as f:
    #tweets = json.load(f)
#with open("tweet_stream_trump_NY_1000.json") as f:
    #tweets = json.load(f)
#with open("tweet_stream_trump_GA_1000.json") as f:
    #tweets = json.load(f)
#with open("tweet_stream_trump_CA_1000.json") as f:
    #tweets = json.load(f)
#with open("tweet_stream_trump_ILI_1000.json") as f:
    #tweets = json.load(f)
    #Loop through the tweets
    for tweet in tweets:
        #Extract the tweet text
        tweetTxt =  tweet['text']
        #Code to ignore the unprocessable UTF-8 character, below code fragment from stackoverflow, referenced above
        tweetTxt =  tweetTxt.encode('ascii', 'ignore').decode('ascii')
        #Split the words in Tweet text
        wordsInTwt = tweetTxt.split()
        #Loop through the words in tweet text
        for word in wordsInTwt:
            #Tried and ignored stemming as per our judgement
            #word = ss.stem(word)
            #Append the word to wordLst that was created previously
            wordLst.append(word)
        #Increment and print the number of tweets processed for tracking purposes
        tweetsProcessed+=1
        print tweetsProcessed
    #For each word in the word list
    for word in wordLst:
        #Convert the word to lower case to deal with case sensitivity
        lowerWord = word.lower()
        #Remove the words that is of length 1 and stop words including additional frequently occuring words. 
        if len(lowerWord) == 1 or lowerWord in stopwords or 'via' in lowerWord or 'trump' in lowerWord or 'amp' in lowerWord or 'http' in lowerWord or 'https' in lowerWord or 'donald' in lowerWord or 'retweet' in lowerWord or 'rt' in lowerWord or '@' in lowerWord or 'president' in lowerWord:
            continue
        #Append the word to text if the word meets the above fiter criteria
        text += '{} '.format(word)

#Create word cloud with max font size as 40 using the text
wordcloud = WordCloud(max_font_size=40).generate(text) 

# Plot the word clound using the pyplot from matplotlib
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()