'''
Team 13, Melbourne
Jing Qiu, 1152016, jiqiu1@student.unimelb.edu.au
Meijun Yue, 1190161, meijuny@student.unimelb.edu.au
Suyi Jiao, 1222833, sjjiao@student.unimelb.edu.au
Yeting Wu, 1310061, yetingw@student.unimelb.edu.au
Wenshuo Pan, 1226506, wenshuop@student.unimelb.edu.au
'''

from wordcloud import WordCloud, STOPWORDS
import couchdb

def backend_get_wordcloud(db, city, year, month, type):
    # set document id, e.g. 'darwin_2021-01_covid'
    time = str(year) + '-' + '{0:02d}'.format(month)
    doc_id = '{}_{}_{}'.format(city.lower().replace(' ', ''), time, type)

    stopwords = set(STOPWORDS)
    wordcloud_fdict = dict(db.get(doc_id))
    if wordcloud_fdict is not None:
        # drop '_id' and '_rev' from the retrieved dictionary
        wordcloud_fdict.pop('_id', None)
        wordcloud_fdict.pop('_rev', None)
        wc = WordCloud(width=800, height=400, max_words=50, stopwords=stopwords, background_color='floralwhite').generate_from_frequencies(wordcloud_fdict)
        wc.to_file('{}_wordcloud.png'.format(doc_id))
    else:
        print('document does not exit.')


if __name__ == '__main__':
    server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')
    db = server['wordcloud']

    # set parameters
    city = 'Melbourne'
    year = 2022
    month = 1
    type = 'covid'

    backend_get_wordcloud(db, city, year, month, type)
