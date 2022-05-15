'''
Team 13, Melbourne
Jing Qiu, 1152016, jiqiu1@student.unimelb.edu.au
Meijun Yue, 1190161, meijuny@student.unimelb.edu.au
Suyi Jiao, 1222833, sjjiao@student.unimelb.edu.au
Yeting Wu, 1310061, yetingw@student.unimelb.edu.au
Wenshuo Pan, 1226506, wenshuop@student.unimelb.edu.au
'''

import json
import couchdb
from collections import defaultdict
from tweepy import StreamRule, StreamingClient

# import classifier
import sys
sys.path.append('../../classifier')
from sentiment_classifier import TweetProcessor

# class TweetStreaming
class TweetStreaming(StreamingClient):
    def __init__(self, bearer_token):
        StreamingClient.__init__(self, bearer_token=bearer_token, wait_on_rate_limit=True)
        self.tweet_processor = TweetProcessor()
        self.server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')
        self.cities = self.load_cities("australia_cities.json")

    # read the city information from file "australia_cities.json"
    def load_cities(self, file_name):
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
    def find_or_create_db(self, db):
        if db in self.server:
            return self.server[db]
        else:
            return self.server.create(db)

    def on_tweet(self, tweet):
        city_id = tweet.geo['place_id']
        city_details = self.cities[city_id]
        # check if the tweet is located at our 8 cities
        if city_details:
            tweet = {'_id': str(tweet.id),
                     'created_at': str(tweet.created_at),
                     'text': tweet.text,
                     'city_name': city_details['name'],
                     'city_id': city_id,
                     'city_full_name': city_details['full_name']
                     }
            tweet = self.tweet_processor.process(tweet)
            # save each tweet into corresponding database (named as city)
            db = self.find_or_create_db(city_details['name'].lower().replace(' ', ''))
            if tweet['_id'] not in db:
                db.save(tweet)

    def on_request_error(self, status_code):
        print("stream request error, HTTP status code", status_code)

    def on_connection_error(self):
        print("stream connection errors or times out")
        self.disconnect()

if __name__ == "__main__":
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAOXibwEAAAAAaCPX7W8EsUIUh1jXeGE2OboACuI%3DXJ9BoTzhi2OXh7C3J7AUoEATEjnqhUkgtjeLO4WBRDn0ce1w8Y"
    client = TweetStreaming(bearer_token)

    # Remove existing rules
    # Set new rules & check the rule (get all tweets located at AU)

    # resp = client.get_rules()
    # if resp and resp.data:
    #     rule_ids = []
    #     for rule in resp.data:
    #         rule_ids.append(rule.id)
    #     client.delete_rules(rule_ids)
    # rule = StreamRule(value="lang:en place_country:AU")
    # resp = client.add_rules(rule)
    # if resp.errors:
    #     raise RuntimeError(resp.errors)
    # resp = client.get_rules()
    # print(resp.data)

    # fetch real-time streaming tweets, process and store to the databases
    try:
        client.filter(backfill_minutes=5, tweet_fields=["created_at", "geo"])
    except KeyboardInterrupt:
        client.disconnect()

