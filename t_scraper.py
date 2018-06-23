import tweepy
import json
from tweepy import OAuthHandler

def prune_json(tweet_json, search_results):
    new_json = {
        'created_at': tweet_json['created_at'],
        'id': tweet_json['id'],
        'text': tweet_json['text'],
        'entities': {
            'hashtags': tweet_json['entities']['hashtags'],
            'user_mentions': tweet_json['entities']['user_mentions'],
        },
        'in_reply_to_status_id': tweet_json['in_reply_to_status_id'],
        'in_reply_to_user_id': tweet_json['in_reply_to_user_id'],
        'user': {
            'id': tweet_json['user']['id'],
            'screen_name': tweet_json['user']['screen_name'],
            'followers_count': tweet_json['user']['followers_count'],
            'friends_count': tweet_json['user']['friends_count'],
            'created_at': tweet_json['user']['created_at'],
            'verified': tweet_json['user']['verified'],
        },
        'geo': tweet_json['geo'],
        'retweet_count': tweet_json['retweet_count'],
        'favorite_count': tweet_json['favorite_count'],
    }

    return new_json

def search_query():
    query = input("enter query to search for (please include # for hashtags)\n")
    plain_query = ''.join(char for char in query if char.isalnum())
    tweet_count = int(input("how many tweets to return\n"))
    search_results = [tweet._json for tweet in tweepy.Cursor(api.search, q=query).items(tweet_count)]
    outfile = open('bulk_query_' + plain_query + '_results.txt', 'w')
    outfile.close()
    outfile = open('bulk_query_' + plain_query + '_results.txt', 'r+')

    for tweet_json in search_results:
        new_json = prune_json(tweet_json, search_results)
        outfile.write('{ "index" : { "_index" : "tweets", "_type" : "tweet" } }\n')
        json.dump(new_json, outfile)
        outfile.write('\n')
    return

def search_user():
    handle = input("enter twitter screen_name (@name_here) of user to scrape all tweets for (please omit the @)\n")
    search_results = [tweet._json for tweet in tweepy.Cursor(api.user_timeline, screen_name='@' + handle).items()]
    outfile = open('bulk_user_' + handle + '_results.txt', 'w')
    outfile.close()
    outfile = open('bulk_user_' + handle + '_results.txt', 'r+')

    for tweet_json in search_results:
        new_json = prune_json(tweet_json, search_results)
        outfile.write('{ "index" : { "_index" : "tweets", "_type" : "tweet" } }\n')
        json.dump(new_json, outfile)
        outfile.write('\n')
    return

consumer_key = 'Bxk5A1a0K2p7Y3ZD5PY4qtp2d'
consumer_secret = 'DqCN4XmSYXhvTAUSl9eS3ul3tcOYXBkWjfT8ZqtjUMczapkGtc'
access_token = '858968490941718528-6C7TRZ6jhZAcxjC6jCmXWu9c0zzVLq5'
access_secret = '7Wckd14wQ51WbCY05zIqU3UGMIv2OLfb2zUsvy1vXJHIq'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

while True:
    #prompt user for choice of function
    while True:
        try:
            function_choice = int(input("Enter 0 to search by query or enter 1 to search by @user\n"))
        except ValueError:
            print ("Please enter 0 or 1 only\n")
            continue

        if function_choice == 0 or function_choice == 1:
            break
        else:
            continue
    if function_choice == 0:
        search_query()
    if function_choice == 1:
        search_user()

    #prompt user to search again
    while True:
        try:
            continue_choice = int(input("Enter 0 to start a new search or enter 1 to quit\n"))
        except ValueError:
            print("Please enter 0 or 1 only\n")
            continue

        if continue_choice == 0:
            break
        if continue_choice == 1:
            quit(0)
        else:
            continue