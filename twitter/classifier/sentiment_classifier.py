'''
Team 13, Melbourne
Jing Qiu, 1152016, jiqiu1@student.unimelb.edu.au
Meijun Yue, 1190161, meijuny@student.unimelb.edu.au
Suyi Jiao, 1222833, sjjiao@student.unimelb.edu.au
Yeting Wu, 1310061, yetingw@student.unimelb.edu.au
Wenshuo Pan, 1226506, wenshuop@student.unimelb.edu.au
'''

import os.path
import re
import string
import nltk
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
nltk.download(['wordnet', 'omw-1.4', 'averaged_perceptron_tagger', 'stopwords', 'punkt', 'vader_lexicon'])

# a TweetProcessor class to process raw tweet,
# do tokenization/normalization on tweet text, sentiment/subjectivity analysis, and analyse whether covid-related
class TweetProcessor:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.tokenizer = TweetTokenizer()
        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = nltk.corpus.stopwords.words('english') + list(string.punctuation)
        self.covid_keywords = self.load_covid_keywords()
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

    def load_covid_keywords(self):
        file_path = os.path.dirname(__file__) + '/covid_keywords.txt'
        covid_keywords = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for word in f.readlines():
                covid_keywords.append(word.rstrip())
        return covid_keywords

    # do sentiment analysis, subjectivity analysis, covid-related and text normalization
    def process(self, tweet):
        tweet['text'] = re.sub(r'\s+', ' ', tweet['text'])               # remove newline/tab characters to whitespace
        tweet['text'] = re.sub(r'https?:\/\/\S*', '', tweet['text'])     # remove urls
        tweet['text'] = re.sub(r'@[^\s]+', '', tweet['text'])            # remove mentions @mention

        # analyse sentiment with NLTK Vader
        # (vader does not require much preprocessing, it can understand emojis, punctuation and capital case)
        tweet = self.sentiment_classify(tweet)
        # subjectivity classification with Textblob
        tweet = self.subjectivity_classify(tweet)

        tweet['text'] = tweet['text'].lower()                            # lowercase
        tweet['text'] = self.emoji_pattern.sub(r' ', tweet['text'])      # remove emojis

        # check if the tweet is covid-related
        tweet = self.is_covid_related(tweet)

        # tokenize and normalize text
        tweet = self.normalize(tweet)
        return tweet

    # predict sentiment(polarity) using nltk pre-trained vader classifier
    # neg, neu, pos score in range [0.0, 1.0], compound score in range [-1.0, 1.0]
    # sentiment_vader label is assigned to pos/neg/neu based on the compound score
    def sentiment_classify(self, tweet):
        scores = self.sia.polarity_scores(tweet['text'])
        tweet['neg'] = scores['neg']
        tweet['neu'] = scores['neu']
        tweet['pos'] = scores['pos']
        tweet['compound'] = scores['compound']
        if scores['compound'] >= 0.05:
            tweet['sentiment_vader'] = 'pos'
        elif scores['compound'] <= -0.05:
            tweet['sentiment_vader'] = 'neg'
        else:
            tweet['sentiment_vader'] = 'neu'
        return tweet

    # predict polarity/subjectivity score using TextBlob
    # polarity score is a float within the range [-1.0, 1.0]
    # subjectivity is a float within the range [0.0, 1.0], where 0 is very objective and 1 is very subjective.
    def subjectivity_classify(self, tweet):
        blob = TextBlob(tweet['text'])
        tweet['polarity_blob'] = blob.sentiment.polarity
        tweet['subjectivity_blob'] = blob.sentiment.subjectivity
        return tweet

    def is_covid_related(self, tweet):
        text = tweet['text']
        for k in self.covid_keywords:
            if k in text:
                tweet['covid'] = 'true'
                return tweet
        tweet['covid'] = 'false'
        return tweet

    # preprocessing raw text: tokenize and normalize text
    def normalize(self, tweet):
        text = tweet['text']
        # tokenize
        tokens = self.tokenizer.tokenize(text)
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
        normalized_tokens = [t for t in tokens if t not in self.stopwords and re.search(r'[a-z0-9]+', t)]
        tweet['text'] = ' '.join(normalized_tokens)
        return tweet
