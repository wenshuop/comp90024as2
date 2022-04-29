import tweepy
import json
import couchdb
import pandas as pd
from collections import defaultdict
from datetime import datetime, timedelta

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
def find_or_create_db(server, db_name):
    if db_name in server:
        return server[db_name]
    else:
        return server.create(db_name)

# save each tweet into the database
def save_tweet(database, tweet, city_id, city_details):
    if str(tweet.id) not in database:
        id, rev = database.save({"_id": str(tweet.id),
                                 "created_at": str(tweet.created_at),
                                 "text": tweet.text,
                                 "city_name": city_details['name'],
                                 "city_id": city_id,
                                 "city_full_name": city_details["full_name"],
                                 "city_coordinates": city_details["bounding_box"]})
        # print("tweet saved", id)

# load search start/end time from file "search_start_times.csv"
def load_search_times(file_name, city):
    df = pd.read_csv(file_name, names=["city", "start_time", "end_time"])
    for idx in df.index:
        if df.at[idx, 'city'] == city:
            start_time = df.at[idx, 'start_time']
            end_time = df.at[idx, 'end_time']
    try:
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
    except:
        end_time, start_time = (datetime.now() - timedelta(days=1)), (datetime.now() - timedelta(days=30))
    return start_time, end_time

# update next search time for a specific city to "search_start_times.csv"
def update_search_times(file_name, city, end_time):
    df = pd.read_csv(file_name, names=["city", "start_time", "end_time"])
    for idx in df.index:
        if df.at[idx, 'city'] == city:
            df.at[idx, 'start_time'] = end_time - timedelta(days=30)
            df.at[idx, 'end_time'] = end_time
    df.to_csv(file_name, header=False, index=False)


if __name__ == '__main__':
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAOXibwEAAAAAaCPX7W8EsUIUh1jXeGE2OboACuI%3DXJ9BoTzhi2OXh7C3J7AUoEATEjnqhUkgtjeLO4WBRDn0ce1w8Y"
    client = tweepy.Client(bearer_token, wait_on_rate_limit=True)
    server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')
    database = find_or_create_db(server, 'twitter')

    # iteratively harvest tweets through cities by month
    cities = load_cities("australia_cities.json")
    break_loop = False
    while True:
        for city_id, city_details in cities.items():
            query = "lang:en place:" + city_id
            # load search time from "search_start_times.csv"
            start_time, end_time = load_search_times("search_start_times.csv", city_details['name'])
            if end_time.year < 2021:
                break_loop = True
                continue
            else:
                break_loop = False
            resp = client.search_all_tweets(query, tweet_fields=["created_at", "geo"], max_results=500,
                                            start_time=start_time, end_time=end_time)
            if resp.errors:
                raise RuntimeError(resp.errors)
            if resp.data:
                for tweet in resp.data:
                    save_tweet(database, tweet, city_id, city_details)

            while 'next_token' in resp.meta:
                resp = client.search_all_tweets(query, tweet_fields=["created_at", "geo"], max_results=500,
                                                start_time=start_time, end_time=end_time,
                                                next_token=resp.meta["next_token"])
                if resp.errors:
                    raise RuntimeError(resp.errors)
                if resp.data:
                    for tweet in resp.data:
                        save_tweet(database, tweet, city_id, city_details)

            # update the search time for this city in "search_start_times.csv"
            update_search_times("search_start_times.csv", city_details['name'], start_time)
            print(city_details['name'], "tweets harvest finished from", start_time, "to", end_time)

        if break_loop:
            break

    print("Tweet Search end.")