import couchdb
from sentiment_classifier import TweetProcessor

# clean and process the raw tweet from a database and store the cleaned data into new database
class TweetCleaner:
    def __init__(self, server, db):
        self.processor = TweetProcessor()
        self.server = couchdb.Server(server)
        self.db = self.find_db(db)
        self.newdb = None

    def set_new_db(self, newdb):
        self.newdb = self.find_or_create_db(newdb)

    # get specified database, or None if not exit
    def find_db(self, db):
        if db in self.server:
            return self.server[db]
        else:
            print('the database {} does not exit'.format(db))
            return None

    # get specified database, or create a new database if not exit
    def find_or_create_db(self, db):
        if db in self.server:
            return self.server[db]
        else:
            return self.server.create(db)

    def get_tweets_id(self, view, city, year, month):
        start_date = str(year) + '-' + '{0:02d}'.format(month)
        end_date = str(year) + '-' + '{0:02d}'.format(month+1)
        view = self.db.view(view, group=True, group_level=3,
                            start_key=[city, start_date], end_key=[city, end_date])
        print('the total number of raw tweets retrieved is {}'.format(len(view)))
        id_lst = [item.key[2] for item in view]
        return id_lst

    def clean_tweets(self, view, city, year, month):
        print('Process and clean tweets located at {} Y {} M {}.'.format(city, year, month))
        id_lst = self.get_tweets_id(view, city, year, month)
        for id in id_lst:
            tweet = dict(self.db[id])
            tweet_new = self.processor.process(tweet)
            self.newdb.save(tweet_new)
        print('Process tweets finished.')


if __name__ == '__main__':
    server = 'http://admin:admin@172.26.128.22:5984//'
    db = 'twitter'
    cleaner = TweetCleaner(server, db)

    year_lst = [2021, 2022]
    month_lst = list(range(1, 13))
    date_lst = [(y, m) for y in year_lst for m in month_lst]
    city_lst = ['Adelaide', 'Brisbane', 'Canberra', 'Darwin', 'Hobart', 'Melbourne', 'Perth (WA)', 'Sydney']

    view = 'tweet_stats/count_city_month'
    for year, month in date_lst:
        for city in city_lst:
            cleaner.set_new_db(city.lower())
            cleaner.clean_tweets(view, city, year, month)
