from twython import TwythonStreamer
"""
References:
https://www.dropbox.com/sh/cpkokzf1ko0p53t/AABjaP2zGlQKtCePrm08nB-Xa/JG_Ch09_Getting_Data/04_api/3_test_twitter_stream.py?dl=0
"""
#Import the necessary packages
import simplejson as json

#Create an empty list, collected tweets will be added to this list. 
collectedTweets = []
#Create customer class tweetStreamer which inherits from Twython Streamer
class tweetStreamer(TwythonStreamer):
 
    # override the on_success method of Twython Streamer as per our requirement
    def on_success(self, data):
        #Check if the incoming JSON has Lang parameter and if it equals 'en'
        if 'lang' in data and data['lang'] == 'en':
            #If the above condition is satisfied append the incoming JSON to the list of collected tweets
            collectedTweets.append(data)
            #Print the length of collected tweets for tracking purposes
            print len(collectedTweets)
        #When the collected tweets reach 10000, store the tweets to JSON and disconnect the connection to twitter API through function calls.   
        if len(collectedTweets) >= 10000:
            self.store_json()
            self.disconnect()
 
    # override the on_error method of twython as per our requirement
    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()
    #Store the tweets in a file in JSON format with appropriate filename
    def store_json(self):
        with open('tweet_stream_{}_{}_{}.json'.format('trump','US', len(collectedTweets)), 'w') as f:
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
    #Using a while loop and checking if we reached the required number of tweets as Twitter API gets disconnected frequently. 
    while(len(collectedTweets)<10000):
        #Surround the filter logic with try catch to deal with Twitter streaming API connectivity issues. 
        try:
            #The filter condition with the required keyword for this project.
            tweetCollection.statuses.filter(track='trump')
        except:
            #On exception which is usually a connection issue, igonore the tweet and let the program re connect, so continue
            continue
        