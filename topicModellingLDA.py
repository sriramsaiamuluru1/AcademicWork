from __future__ import division, print_function
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:02:34 2017

@author: sameerkumar

References: 
http://stackoverflow.com/questions/9942594/unicodeencodeerror-ascii-codec-cant-encode-character-u-xa0-in-position-20    
https://www.dropbox.com/sh/cpkokzf1ko0p53t/AAAwhDa14UmfdAA6TW2dcDt4a/JG_Ch20_Text_Mining/0_notebooks/text_part3_topic_modeling_Section001.ipynb?dl=0

"""
#Import All the necessary packages
from gensim import models, corpora
import nltk
import json
import logging
#Logging for tracking purposes
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO
#Get the stopwords from NLTK
stopwords = nltk.corpus.stopwords.words('english')
#Create an empty list of proceesed tweets, will be used later.
processedTweets = []
#Create a counter variable for tracking purposes
tweetsProcessed = 0

#Import the JSON and load the tweets from the JSON file
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
        #Create a text variable for each tweet will be used to reconstruct the tweet after removing stopwords
        text = ''
        #Extract the tweet text
        tweetTxt =  tweet['text']
        #Below line of code added to deal with UTF-8 Processing error, referenced above from stackoverflow
        tweetTxt =  tweetTxt.encode('ascii', 'ignore').decode('ascii')
        #Split the words in the tweet text
        wordsInTwt = tweetTxt.split()
        #Loop through the words in the tweet
        for word in wordsInTwt:
            #Convert the word to lower case to deal with case sensitivity
            lowerWord = word.lower()
            #Filter the words with length 1 and stop words from NLTK and other necessary words that occur frequently.
            if len(lowerWord) == 1 or lowerWord in stopwords or 'via' in lowerWord  or 'amp' in lowerWord or 'http' in lowerWord or 'https' in lowerWord  or 'retweet' in lowerWord or 'rt' in lowerWord or '@' in lowerWord :
                continue
            #Reconstruct the tweet with the words that meet the above filtering criteria
            text += '{} '.format(word)
        #Append the reconstructed tweet to the list that was created above
        processedTweets.append(text.strip())
        #Increment and print the number of tweets processed for tracking purposes
        tweetsProcessed+=1
        print (tweetsProcessed)
    #Create a dictionary with the list of reconstructed tweets.
    dic = corpora.Dictionary([processedTweets])
    #Convert the dictionary to a bag of words. 
    corpus = [dic.doc2bow([processedTweet]) for processedTweet in processedTweets]
    #Calculate the tfidf score for  the tweet corpus
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    #Choose the number of topics to be reported by the model
    NUM_TOPICS = 24
    #Build the LDA model with 100 passes
    model = models.ldamodel.LdaModel(corpus_tfidf, 
                                 num_topics=NUM_TOPICS, 
                                 id2word=dic, 
                                 update_every=1, 
                                 passes=100)
    #Print the model Output
    print("Model Output")
    topics_found = model.print_topics(24)
    counter = 1
    for t in topics_found:
        print("Topic #{} {}".format(counter, t))
        counter += 1
    model.print_topics()