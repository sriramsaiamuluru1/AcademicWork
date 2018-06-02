from twython import TwythonStreamer
"""
References:
https://www.dropbox.com/sh/cpkokzf1ko0p53t/AABjaP2zGlQKtCePrm08nB-Xa/JG_Ch09_Getting_Data/04_api/3_test_twitter_stream.py?dl=0
"""
#Import the necessary packages
import json
#Create an empty list, collected tweets will be added to this list.
collectedTweets = []
#This is a variable that is used for tracking purposes to make sure that the program is collecting tweets. 
numTweetsAnalyzed = 0
#Create customer class tweetStreamer which inherits from Twython Streamer
class tweetStreamer(TwythonStreamer):
 
    # override the on_success method of Twython Streamer as per our requirement
    def on_success(self, data):
        #Use the global variable which we created above
        global numTweetsAnalyzed
        #Increment and print the variable to track the number of tweets processed for tracking purposes.
        numTweetsAnalyzed+=1
        print numTweetsAnalyzed
        #Check if the incoming JSON has Lang parameter and if it equals 'en' and our keyword which is trump in this case is present in the incoming tweet in lower case add it to the tweet collection list
        if 'lang' in data and data['lang'] == 'en'and 'text' in data and 'trump' in data['text'].lower():
            #If the above condition is satisfied append the incoming JSON to the list of collected tweets
            collectedTweets.append(data)
            #Print the length of collected tweets for tracking purposes
            print len(collectedTweets)
            
        #When the collected tweets reach 1000, store the tweets to JSON and disconnect the connection to twitter API through function calls.
        if len(collectedTweets) >= 1000:
            self.store_json()
            self.disconnect()
 
    # override the on_error method of twython as per our requirement
    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()
    #Store the tweets in a file in JSON format with appropriate filename    
    def store_json(self):
        with open('tweet_stream_{}_{}_{}.json'.format('trump','GA', len(collectedTweets)), 'w') as f:
            json.dump(collectedTweets, f, indent=5)
 
#If the program is running from command line, which it will, perform the below
if __name__ == '__main__':
    #Open the twitter credentials file and load the credentials
    with open('myTwitterCredentials.json', 'r') as f:
    
        credentials = json.load(f)
 
    # consumer key, consumer secret, access token and access token secret of our app
    CONSUMER_KEY = credentials['CONSUMER_KEY']
    CONSUMER_SECRET = credentials['CONSUMER_SECRET']
    ACCESS_TOKEN = credentials['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = credentials['ACCESS_TOKEN_SECRET']
    #Create a live stream with Twitter API using the credentials
    tweetCollection = tweetStreamer(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    #Using a while loop and checking if we reached the required number of tweets as Twitter API gets disconnected frequently
    while(len(collectedTweets)<1000):
        #Surround the filter logic with try catch to deal with Twitter streaming API connectivity issues. 
        try:
            #Filter by location using the latitude and longitude of southwest and north east points from the state of Georgia
            tweetCollection.statuses.filter(locations=[-84.924316,32.634171,-83.386230,34.718476])
        except:
            #On exception which is usually a connection issue, igonore the tweet and let the program re connect, so continue
            continue
        