'''
Team 13, Melbourne
Jing Qiu, 1152016, jiqiu1@student.unimelb.edu.au
Meijun Yue, 1190161, meijuny@student.unimelb.edu.au
Suyi Jiao, 1222833, sjjiao@student.unimelb.edu.au
Yeting Wu, 1310061, yetingw@student.unimelb.edu.au
Wenshuo Pan, 1226506, wenshuop@student.unimelb.edu.au
'''

import collections
import couchdb
import re
import string
import nltk
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn
from wordcloud import WordCloud
# nltk.download(['wordnet', 'omw-1.4', 'averaged_perceptron_tagger', 'stopwords', 'punkt'])

# get specified database, return None if the database does not exit
def find_db(server, db):
    if db in server:
        return server[db]
    else:
        return None

# get a database if exits, or create a new database if not exits
def find_or_create_db(server, db):
    if db in server:
        return server[db]
    else:
        return server.create(db)

# update an existing document in the given database
def save_or_update(db, doc):
    if doc['_id'] in db:
        doc_old = db.get(doc['_id'])
        doc['_rev'] = doc_old['_rev']
        db.save(doc)
    else:
        db.save(doc)

def get_ids(server, city, year, month, type):
    db = find_db(server, city.lower().replace(' ', ''))
    start_key = [str(year) + '-' + '{0:02d}'.format(month)]
    end_key = [str(year) + '-' + '{0:02d}'.format(month + 1)]
    view = db.view('{0}/{0}_count'.format(type), reduce=False, start_key=start_key, end_key=end_key, include_docs=True)
    ids = []
    for row in view:
        ids.append(row.id)
    print('retrieving tweet ids from {}/{}/{}/{}, total number {}'.format(city, year, month, type, len(ids)))
    return ids

def get_raw_text(server, db, ids):
    db = find_db(server, db)
    raw_text = []
    for id in ids:
        tweet = db.get(id)
        if tweet is not None:
            raw_text.append(tweet['text'])
    print('retrieving raw tweet text, total number {}'.format(len(raw_text)))
    return raw_text

class TweetProcessor():
    def __init__(self):
        self.tokenizer = TweetTokenizer()
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = nltk.corpus.stopwords.words('english') + list(string.punctuation)
        self.emoji_pattern = re.compile("["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        u"\U00002500-\U00002BEF"  # chinese char
                                        u"\U00002702-\U000027B0"
                                        u"\U00002702-\U000027B0"
                                        u"\U000024C2-\U0001F251"
                                        u"\U0001f926-\U0001f937"
                                        u"\U00010000-\U0010ffff"
                                        u"\u2640-\u2642"
                                        u"\u2600-\u2B55"
                                        u"\u200d"
                                        u"\u23cf"
                                        u"\u23e9"
                                        u"\u231a"
                                        u"\ufe0f"  # dingbats
                                        u"\u3030"
                                        "]+", flags=re.UNICODE)

    def normalize(self, text, type):
        new_text = []
        for str in text:
            str = self.emoji_pattern.sub(r' ', str)                 # remove emojis
            str = re.sub(r'https?:\/\/\S*', '', str)                # remove urls
            str = re.sub(r'@[^\s]+', '', str)                       # remove mentions @mention
            str = re.sub(r'\s+', ' ', str)                          # remove newline/tab characters to whitespace
            str = str.lower()                                       # lowercase

            # tokenize and normalize text
            tokens = self.tokenizer.tokenize(str)
            # keep hashtag but remove the start_with symbol '#'
            for i in range(len(tokens)):
                if tokens[i].startswith('#'):
                    tokens[i] = tokens[i][1:]
            # lemmatize (using pos tag)
            tag_map = defaultdict(lambda: wn.NOUN)
            tag_map['J'] = wn.ADJ
            tag_map['V'] = wn.VERB
            tag_map['R'] = wn.ADV
            tokens_tags = pos_tag(tokens)
            tokens = [self.lemmatizer.lemmatize(token, tag_map[tag[0]]) for token, tag in tokens_tags]
            # remove stopwords (including punctuation)
            # remove keywords 'covid' if type == 'covid'
            if type == 'covid':
                normalized_tokens = [t for t in tokens if t not in self.stopwords and re.search(r'[a-z0-9]+', t) and t != 'covid']
            else:
                normalized_tokens = [t for t in tokens if t not in self.stopwords and re.search(r'[a-z0-9]+', t)]
            str = ' '.join(normalized_tokens)
            new_text.append(str)

        print('normalizing tweet text, total number {}'.format(len(new_text)))
        return new_text

def wordcloud(text):
    wordcloud = collections.defaultdict()
    for row in text:
        tokens = row.split()
        for t in tokens:
            if t.startswith('_'):   #couchdb does not accept the document key staring with '_' which means system variable
                continue
            wordcloud[t] = wordcloud.get(t, 0) + 1
    print('extracting term frequencies, total number of term {}, total term counts {}'.format(len(wordcloud), sum(wordcloud.values())))
    return wordcloud

def topic_analysis(text, n_features=1000, n_components=5, n_top_words=20):
    # Use tf (raw term count) features for LDA.
    tf_vectorizer = CountVectorizer(ngram_range=(1, 1), max_df=0.95, min_df=2, max_features=n_features)
    tf = tf_vectorizer.fit_transform(text)
    # Fit LDA model
    lda = LatentDirichletAllocation(n_components=n_components,
                                    learning_method="online", max_iter=10, learning_offset=50.0, random_state=0)
    lda.fit(tf)

    # Get topics visualization
    topic_vis = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer, R=n_top_words)
    topic_vis = topic_vis.to_dict()

    # Get topics dictionary
    feature_names = tf_vectorizer.get_feature_names()
    topic_dict = dict()
    for topic_idx, topic in enumerate(lda.components_):
        top_features_ind = topic.argsort()[: -n_top_words - 1: -1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind].tolist()
        topic_dict[topic_idx] = [top_features, weights]

    return topic_dict, topic_vis


if __name__ == '__main__':
    processor = TweetProcessor()
    server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')
    db_wordcloud = find_or_create_db(server, 'wordcloud')
    db_topic_dict = find_or_create_db(server, 'topic_dict')
    db_topic_vis = find_or_create_db(server, 'topic_vis')

    # set parameters
    city = 'Melbourne'
    year = 2021
    month = 1
    type = 'covid'

    for year in [2021, 2022]:
        for month in range(1, 13, 1):
            if year == 2022 and month > 4:
                break
            # set document id, e.g. 'darwin_2021-01_covid'
            time = str(year) + '-' + '{0:02d}'.format(month)
            doc_id = '{}_{}_{}'.format(city.lower().replace(' ', ''), time, type)
            print('id: ', doc_id)

            # get ids --> get raw text --> normalize/tokenize text
            id_lst = get_ids(server, city, year, month, type)
            text = get_raw_text(server, 'twitter', id_lst)
            text = processor.normalize(text, type)
            # if it's to analyse covid-related tweet, then keyword 'covid' will be deleted from both wordcloud and topics

            # extract WordCloud Frequency Dictionary
            wordcloud_fdict = wordcloud(text)
            wordcloud_fdict['_id'] = doc_id
            save_or_update(db_wordcloud, wordcloud_fdict)

            # train LDA model, get Topics Dictionary + LDA Visulization
            topic_dict, topic_vis = topic_analysis(text, n_features=1000, n_components=5, n_top_words=20)
            topic_dict['_id'] = doc_id
            topic_vis['_id'] = doc_id
            save_or_update(db_topic_dict, topic_dict)
            save_or_update(db_topic_vis, topic_vis)


