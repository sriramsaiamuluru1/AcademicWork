import json
from textblob import TextBlob
import matplotlib.pyplot as plt
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 13:06:12 2017

@author: sameerkumar

References:
https://www.dropbox.com/sh/cpkokzf1ko0p53t/AAB4a6w6bO54iGC-7AgPzhh-a/JG_Ch20_Text_Mining/0_notebooks/text_part1_nltk_textblob_wordcloud_section001.ipynb?dl=0
"""
#Create an empty list to capture Subjectivity score. 
sub_lst = []
#Create an empty list to capture Polarity Score
pol_lst = []
#Counter variable to capture the number of tweets processed for tracking purposes.
processedTwt = 0
#Open the JSON file and the load the tweets in JSON format
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
    #For each of the tweets from list of tweets retrieved from JSON file
    for tweet in tweets:
        #Get the text of the tweet
        tweetTxt =  tweet['text']
        #Create a text blob with the tweet text
        tblob = TextBlob(tweetTxt)
        #Append the subjectivity score from the textblob to the appropriate list.
        sub_lst.append(tblob.sentiment.subjectivity)
        #Append the Polarity score from the textblob to the appropriate list. 
        pol_lst.append(tblob.sentiment.polarity)
        #Increment and print the processed tweet counter for tracking purposes
        processedTwt+=1
        print processedTwt

#Calculate the average of subjectivity score and report it at the bottom of the plot. 
sub_lst_average = sum(sub_lst)/len(sub_lst)    
#Plot the Subjecitivity
plt.title('Sentiment Analysis For United States\n Subjectivity Score')
#plt.title('Sentiment Analysis For Illinois\n Subjectivity Score')
#plt.title('Sentiment Analysis For California\n Subjectivity Score')
#plt.title('Sentiment Analysis For New York\n Subjectivity Score')
#plt.title('Sentiment Analysis For Texas\n Subjectivity Score') 
#plt.title('Sentiment Analysis For Georgia\n Subjectivity Score')   
plt.hist(sub_lst, bins=25)
plt.xlabel('subjectivity score \n Average Subjectivity Score : {}'.format(sub_lst_average))
plt.ylabel('tweet count')
plt.grid(True)
plt.show()

#Calculate the average of polarity score and report it at the bottom of the plot. 
pol_lst_avg = sum(pol_lst)/len(pol_lst)
#Plot the Polarity
plt.title('Sentiment Analysis For United States\n Polarity Score')
#plt.title('Sentiment Analysis For Illinois\n Polarity Score')
#plt.title('Sentiment Analysis For California\n Polarity Score')
#plt.title('Sentiment Analysis For New York\n Polarity Score')
#plt.title('Sentiment Analysis For Texas\n Polarity Score')
#plt.title('Sentiment Analysis For Georgia\n Polarity Score')
plt.hist(pol_lst, bins=25)
plt.xlabel('Polarity score \n Average Polarity Score : {}'.format(pol_lst_avg))
plt.ylabel('tweet count')
plt.grid(True)
plt.show()