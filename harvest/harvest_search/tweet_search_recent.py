import tweepy
import json
import couchdb
import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta
from classifier.sentiment_classifier import TweetProcessor

# read the city information from file "australia_cities.json"
def load_cities(file_name):
    with open(file_name) as f:
        file = json.load(f)
        cities = defaultdict(lambda: dict())
        for city in file:
            id = city['id']
            cities[id]['name'] = city['name']
            cities[id]['full_name'] = city['full_name']
            lng_lst = []
            lat_lst = []
            for (lng, lat) in city['bounding_box']['coordinates'][0]:
                lng_lst.append(lng)
                lat_lst.append(lat)
            lng_lst.sort()
            lat_lst.sort()
            cities[id]['bounding_box'] = [lng_lst[0], lat_lst[0], lng_lst[-1], lat_lst[-1]]
        return cities

# get a database if exits, or create a new database if not exits
def find_or_create_db(server, db):
    if db in server:
        return server[db]
    else:
        return server.create(db)


if __name__ == '__main__':
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAOXibwEAAAAAaCPX7W8EsUIUh1jXeGE2OboACuI%3DXJ9BoTzhi2OXh7C3J7AUoEATEjnqhUkgtjeLO4WBRDn0ce1w8Y"
    client = tweepy.Client(bearer_token, wait_on_rate_limit=True)
    server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')
    tweet_processor = TweetProcessor()

    # iteratively harvest recent tweets through cities, specify start_time and end_time
    cities = load_cities("australia_cities.json")
    end_time = datetime.now() - timedelta(days=1)
    start_time = end_time - timedelta(days=10)

    for city_id, city_details in cities.items():
        # find the corresponding city database
        db = find_or_create_db(server, city_details['name'].lower().replace(' ', ''))
        query = "lang:en place:" + city_id
        resp = client.search_all_tweets(query, tweet_fields=["created_at", "geo"], max_results=500,
                                        start_time=start_time, end_time=end_time)
        if resp.errors:
            raise RuntimeError(resp.errors)
        if resp.data:
            for tweet in resp.data:
                # clean/process tweet and save to the corresponding city database
                tweet = {'_id': str(tweet.id),
                         'created_at': str(tweet.created_at),
                         'text': tweet.text,
                         'city_name': city_details['name'],
                         'city_id': city_id,
                         'city_full_name': city_details['full_name']
                         }
                tweet = tweet_processor.process(tweet)
                if tweet['_id'] not in db:
                    db.save(tweet)

        while 'next_token' in resp.meta:
            resp = client.search_all_tweets(query, tweet_fields=["created_at", "geo"], max_results=500,
                                            start_time=start_time, end_time=end_time,
                                            next_token=resp.meta["next_token"])
            if resp.errors:
                raise RuntimeError(resp.errors)
            if resp.data:
                for tweet in resp.data:
                    # clean/process tweet and save to the corresponding city database
                    tweet = {'_id': str(tweet.id),
                             'created_at': str(tweet.created_at),
                             'text': tweet.text,
                             'city_name': city_details['name'],
                             'city_id': city_id,
                             'city_full_name': city_details['full_name']
                             }
                    tweet = tweet_processor.process(tweet)
                    if tweet['_id'] not in db:
                        db.save(tweet)
        print(city_details['name'], "recent tweets harvest finished from", start_time, "to", end_time)
    print("Recent Tweet Search end.")