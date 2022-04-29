import json
import couchdb
from collections import defaultdict
from tweepy import StreamRule, StreamingClient

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

# class TweetStreaming
class TweetStreaming(StreamingClient):
    def on_tweet(self, tweet):
        city_id = tweet.geo['place_id']
        city_details = cities[city_id]
        if city_details:
            save_tweet(database, tweet, city_id, city_details)

    def on_request_error(self, status_code):
        print("stream request error, HTTP status code", status_code)

    def on_connection_error(self):
        print("stream connection errors or times out")
        self.disconnect()

if __name__ == "__main__":
    server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')
    database = find_or_create_db(server, 'twitter')
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAOXibwEAAAAAaCPX7W8EsUIUh1jXeGE2OboACuI%3DXJ9BoTzhi2OXh7C3J7AUoEATEjnqhUkgtjeLO4WBRDn0ce1w8Y"
    client = TweetStreaming(bearer_token, wait_on_rate_limit=True)

    # load city information
    cities = load_cities("australia_cities.json")

    # Remove existing rules
    resp = client.get_rules()
    if resp and resp.data:
        rule_ids = []
        for rule in resp.data:
            rule_ids.append(rule.id)
        client.delete_rules(rule_ids)
    # set new rules & check the rule
    rule = StreamRule(value="lang:en place_country:AU")
    resp = client.add_rules(rule)
    if resp.errors:
        raise RuntimeError(resp.errors)
    resp = client.get_rules()
    print(resp.data)

    # fetch real-time streaming tweets
    try:
        client.filter(backfill_minutes=5, tweet_fields=["created_at", "geo"])
    except KeyboardInterrupt:
        client.disconnect()

