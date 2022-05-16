'''
Team 13, Melbourne
Jing Qiu, 1152016, jiqiu1@student.unimelb.edu.au
Meijun Yue, 1190161, meijuny@student.unimelb.edu.au
Suyi Jiao, 1222833, sjjiao@student.unimelb.edu.au
Yeting Wu, 1310061, yetingw@student.unimelb.edu.au
Wenshuo Pan, 1226506, wenshuop@student.unimelb.edu.au
'''

import couchdb
import pandas as pd

# get specified database, or create a new database if not exit
def find_or_create_db(server, db):
    if db in server:
        return server[db]
    else:
        return server.create(db)

# return a pd.DataFrame contains the information of the city, type = "all" or "covid"
def get_result(server, city, type):
    db = find_or_create_db(server, city.lower().replace(' ', ''))

    # get total count & month & id
    view = db.view('{}/{}_count'.format(type, type), group=True, group_level=1)
    month_lst = [row.key[0] for row in view]
    id_lst = ['{}_{}'.format(city.lower().replace(' ', ''), m) for m in month_lst]
    city_lst = [city.lower().replace(' ', '')] * len(id_lst)
    total_lst = [row.value for row in view]

    # get pos/neu/neg count
    pos_lst, neu_lst, neg_lst = [], [], []
    view = db.view('{}/{}_sentiment'.format(type, type), group=True, group_level=2)
    for row in view:
        m, sentiment = row.key
        if sentiment == 'pos':
            pos_lst.append(row.value)
        elif sentiment == 'neu':
            neu_lst.append(row.value)
        elif sentiment == 'neg':
            neg_lst.append(row.value)

    # get sub/obj count
    sub_lst, obj_lst = [], []
    view = db.view('{}/{}_subjectivity'.format(type, type), group=True, group_level=2)
    for row in view:
        m, subjectivity = row.key
        if subjectivity == 'sub':
            sub_lst.append(row.value)
        elif subjectivity == 'obj':
            obj_lst.append(row.value)

    # get (sentiment, subjectivity) count
    view = db.view('{}/{}_sentiment_subjectivity'.format(type, type), group=True, group_level=3)
    pos_sub_lst, pos_obj_lst = [], []
    neu_sub_lst, neu_obj_lst = [], []
    neg_sub_lst, neg_obj_lst = [], []
    for row in view:
        m, sentiment, subjectivity = row.key
        if sentiment == 'pos':
            if subjectivity == 'sub':
                pos_sub_lst.append(row.value)
            elif subjectivity == 'obj':
                pos_obj_lst.append(row.value)
        elif sentiment == 'neu':
            if subjectivity == 'sub':
                neu_sub_lst.append(row.value)
            elif subjectivity == 'obj':
                neu_obj_lst.append(row.value)
        elif sentiment == 'neg':
            if subjectivity == 'sub':
                neg_sub_lst.append(row.value)
            elif subjectivity == 'obj':
                neg_obj_lst.append(row.value)

    # get polarity score (float)
    view = db.view('{}/{}_pol_score'.format(type, type), group=True, group_level=1)
    pol_score_lst = [row.value['sum'] / row.value['count'] for row in view]

    # get subjectivity score (float)
    view = db.view('{}/{}_sub_score'.format(type, type), group=True, group_level=1)
    sub_score_lst = [row.value['sum'] / row.value['count'] for row in view]

    # create a dataframe for all the information
    data = zip(id_lst, city_lst, month_lst, total_lst, pos_lst, neu_lst, neg_lst, sub_lst, obj_lst,
               pos_sub_lst, pos_obj_lst, neu_sub_lst, neu_obj_lst, neg_sub_lst, neg_obj_lst, pol_score_lst,
               sub_score_lst)
    columns = ['_id', 'city', 'month', 'total', 'pos', 'neu', 'neg', 'sub', 'obj',
               'pos_sub', 'pos_obj', 'neu_sub', 'neu_obj', 'neg_sub', 'neg_obj', 'pol_score', 'sub_score']
    df = pd.DataFrame(list(data), columns=columns)
    return df

# update an existing document in the given database
def save_or_update(db, doc):
    if doc['_id'] in db:
        doc_old = db.get(doc['_id'])
        doc['_rev'] = doc_old['_rev']
        db.save(doc)
    else:
        db.save(doc)


if __name__ == '__main__':
    server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')
    results_all = []
    results_covid = []

    city_lst = ['Adelaide', 'Brisbane', 'Canberra', 'Darwin', 'Hobart', 'Melbourne', 'Perth (WA)', 'Sydney']
    for city in city_lst:
        results_all.append(get_result(server, city, 'all'))
        results_covid.append(get_result(server, city, 'covid'))
        print(city)

    # concatenate the dataframes together
    results_all = pd.concat(results_all, ignore_index=True)
    results_covid = pd.concat(results_covid, ignore_index=True)

    # output the dataframe to csv file
    results_all.to_csv('results_all.csv')
    results_covid.to_csv('results_covid.csv')

    # store/update the data to couchdb database
    db_results_all = find_or_create_db(server, 'results_all')
    db_results_covid = find_or_create_db(server, 'results_covid')

    results_all = results_all.to_dict(orient='records')
    for doc in results_all:
        save_or_update(db_results_all, doc)

    results_covid = results_covid.to_dict(orient='records')
    for doc in results_covid:
        save_or_update(db_results_covid, doc)