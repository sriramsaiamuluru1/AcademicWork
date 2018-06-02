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

#Import the required packages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition
import nltk
import numpy as np
import json
#Get the stop words from NLTK
stopwords = nltk.corpus.stopwords.words('english')
#Create an empty list to append the processed tweets, will be used later. 
processedTweets = []
#Counter variable for tracking purposes. 
tweetsProcessed = 0
#Empty list for the topic words, will be used later
topic_words = []
#Number of top words to be reported in each topic, change as necessary
num_top_words = 6
#Open the JSON file and load the list of tweets in JSON format
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
    #Loop through the list of tweets
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
    #Create a TFIDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', min_df=2)  
    #Fit trandform the corpus
    doc_term_matrix = vectorizer.fit_transform(processedTweets)
    #Print the matrix shape which list the number of document and the number of unique words in the corpus
    print (doc_term_matrix.shape)
    #Get the list of unique words
    vocab = vectorizer.get_feature_names() 
    #Number of topics to be reported by the model
    num_topics = 22
    clf = decomposition.NMF(n_components=num_topics, random_state=1)
    doctopic = clf.fit_transform(doc_term_matrix)
    for topic in clf.components_:
        #Getting the indexes that have highest weights
        word_idx = np.argsort(topic)[::-1][0:num_top_words]
        #Appending the topic words to the list that was created earlier
        topic_words.append([vocab[i] for i in word_idx])
    #Print the topics
    for t in range(len(topic_words)):
        print ("Topic {}: {}".format(t, ' '.join(topic_words[t][:15])))
   