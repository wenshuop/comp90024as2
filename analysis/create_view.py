import couchdb
from couchdb.design import ViewDefinition

# get specified database, or create a new database if not exit
def find_or_create_db(server, db):
    if db in server:
        return server[db]
    else:
        return server.create(db)

def create_view(db, design_docid, viewid, map_fun, reduce_fun):
    view = ViewDefinition(design_docid, viewid, map_fun=map_fun, reduce_fun=reduce_fun)
    view.sync(db)
    print(view.get_doc(db))

def create_view_all(db):
    # count tweets per month/day per city
    count_map = '''
        function(doc) {
            var city = doc.city_name;
            var month = doc.created_at.substring(0, 7);
            var day = doc.created_at.substring(0, 10);
            emit([city, month, day], 1);
        }'''
    count_red = '_sum'

    # count tweets per sentiment label neu/neg/pos per month/day
    sentiment_map = '''
        function(doc) {
            var city = doc.city_name;
            var sentiment = doc.sentiment_vader;
            var month = doc.created_at.substring(0, 7);
            var day = doc.created_at.substring(0, 10);
            emit([city, sentiment, month, day], 1);
        }'''
    sentiment_red = '_sum'

    # count tweets per subjectivity label sub/obj per month/day
    subjectivity_map = '''
        function(doc) {
            var city = doc.city_name;
            var subjectivity = 'obj';
            if (doc.subjectivity_blob >= 0.5) {
                subjectivity = 'sub';
            }
            var month = doc.created_at.substring(0, 7);
            var day = doc.created_at.substring(0, 10);
            emit([city, subjectivity, month, day], 1);
        }'''
    subjectivity_red = '_sum'

    # count tweets per (neu/neg/pos, sub/obj) per month/day
    sentiment_subjectivity_map = '''
            function(doc) {
                var city = doc.city_name;
                var sentiment = doc.sentiment_vader;
                var subjectivity = 'obj';
                if (doc.subjectivity_blob >= 0.5) {
                    subjectivity = 'sub';
                }
                var month = doc.created_at.substring(0, 7);
                var day = doc.created_at.substring(0, 10);
                emit([city, sentiment, subjectivity, month, day], 1);
            }'''
    sentiment_subjectivity_red = '_sum'

    # average polarity score of tweets per month/day
    # polarity score - the compound score of Vader Classifier
    pol_score_map = '''
        function(doc) {
            var city = doc.city_name;
            var month = doc.created_at.substring(0, 7);
            var day = doc.created_at.substring(0, 10);
            emit([city, month, day], doc.compound);
        }'''
    pol_score_red = '''
        function(keys, values, rereduce) {
            results = {'sum':0, 'count':0};
            if (rereduce) {
                for (var i = 0; i < values.length; i++) {
                    results.sum += values[i].sum;
                    results.count += values[i].count;
                }
                return results;
            } else {
                results.sum = sum(values);
                results.count = values.length;
                return results;
            } 
        }'''

    # average subjectivity score of tweets per month/day
    # sbujectivity score - the subjectivity score of Textblob model
    sub_score_map = '''
        function(doc) {
            var city = doc.city_name;
            var month = doc.created_at.substring(0, 7);
            var day = doc.created_at.substring(0, 10);
            emit([city, month, day], doc.subjectivity_blob);
        }'''
    sub_score_red = '''
        function(keys, values, rereduce) {
            results = {'sum':0, 'count':0};
            if (rereduce) {
                for (var i = 0; i < values.length; i++) {
                    results.sum += values[i].sum;
                    results.count += values[i].count;
                }
                return results;
            } else {
                results.sum = sum(values);
                results.count = values.length;
                return results;
            } 
        }'''

    create_view(db, '_design/all', 'all_count', count_map, count_red)
    create_view(db, '_design/all', 'all_sentiment', sentiment_map, sentiment_red)
    create_view(db, '_design/all', 'all_subjectivity', subjectivity_map, subjectivity_red)
    create_view(db, '_design/all', 'all_sentiment_subjectivity', sentiment_subjectivity_map, sentiment_subjectivity_red)
    create_view(db, '_design/all', 'all_pol_score', pol_score_map, pol_score_red)
    create_view(db, '_design/all', 'all_sub_score', sub_score_map, sub_score_red)

def create_view_covid(db):
    # count covid-related tweets per month/day per city
    count_map = '''
            function(doc) {
                if (doc.covid === 'true') {
                    var city = doc.city_name;
                    var month = doc.created_at.substring(0, 7);
                    var day = doc.created_at.substring(0, 10);
                    emit([city, month, day], 1);
                }                
            }'''
    count_red = '_sum'

    # count covid-related tweets per sentiment label neu/neg/pos per month/day
    sentiment_map = '''
            function(doc) {
                if (doc.covid === 'true') {
                    var city = doc.city_name;
                    var sentiment = doc.sentiment_vader;
                    var month = doc.created_at.substring(0, 7);
                    var day = doc.created_at.substring(0, 10);
                    emit([city, sentiment, month, day], 1);
                }
            }'''
    sentiment_red = '_sum'

    # count covid-related tweets per subjectivity label sub/obj per month/day
    subjectivity_map = '''
            function(doc) {
                if (doc.covid === 'true') {
                    var city = doc.city_name;
                    var subjectivity = 'obj';
                    if (doc.subjectivity_blob >= 0.5) {
                        subjectivity = 'sub';
                    }
                    var month = doc.created_at.substring(0, 7);
                    var day = doc.created_at.substring(0, 10);
                    emit([city, subjectivity, month, day], 1);
                }
            }'''
    subjectivity_red = '_sum'

    # count covid-related tweets per (neu/neg/pos, sub/obj) per month/day
    sentiment_subjectivity_map = '''
                function(doc) {
                    if (doc.covid === 'true') {
                        var city = doc.city_name;
                        var sentiment = doc.sentiment_vader;
                        var subjectivity = 'obj';
                        if (doc.subjectivity_blob >= 0.5) {
                            subjectivity = 'sub';
                        }
                        var month = doc.created_at.substring(0, 7);
                        var day = doc.created_at.substring(0, 10);
                        emit([city, sentiment, subjectivity, month, day], 1);
                    }
                }'''
    sentiment_subjectivity_red = '_sum'

    # average polarity score of covid-related tweets per month/day
    # polarity score - the compound score of Vader Classifier
    pol_score_map = '''
            function(doc) {
                if (doc.covid === 'true') {
                    var city = doc.city_name;
                    var month = doc.created_at.substring(0, 7);
                    var day = doc.created_at.substring(0, 10);
                    emit([city, month, day], doc.compound);
                }
            }'''
    pol_score_red = '''
            function(keys, values, rereduce) {
                results = {'sum':0, 'count':0};
                if (rereduce) {
                    for (var i = 0; i < values.length; i++) {
                        results.sum += values[i].sum;
                        results.count += values[i].count;
                    }
                    return results;
                } else {
                    results.sum = sum(values);
                    results.count = values.length;
                    return results;
                } 
            }'''

    # average subjectivity score of covid-related tweets per month/day
    # sbujectivity score - the subjectivity score of Textblob model
    sub_score_map = '''
            function(doc) {
                if (doc.covid === 'true') {
                    var city = doc.city_name;
                    var month = doc.created_at.substring(0, 7);
                    var day = doc.created_at.substring(0, 10);
                    emit([city, month, day], doc.subjectivity_blob);
                }
            }'''
    sub_score_red = '''
            function(keys, values, rereduce) {
                results = {'sum':0, 'count':0};
                if (rereduce) {
                    for (var i = 0; i < values.length; i++) {
                        results.sum += values[i].sum;
                        results.count += values[i].count;
                    }
                    return results;
                } else {
                    results.sum = sum(values);
                    results.count = values.length;
                    return results;
                } 
            }'''

    create_view(db, '_design/covid', 'covid_count', count_map, count_red)
    create_view(db, '_design/covid', 'covid_sentiment', sentiment_map, sentiment_red)
    create_view(db, '_design/covid', 'covid_subjectivity', subjectivity_map, subjectivity_red)
    create_view(db, '_design/covid', 'covid_sentiment_subjectivity', sentiment_subjectivity_map, sentiment_subjectivity_red)
    create_view(db, '_design/covid', 'covid_pol_score', pol_score_map, pol_score_red)
    create_view(db, '_design/covid', 'covid_sub_score', sub_score_map, sub_score_red)


if __name__ == '__main__':
    server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')
    city_lst = ['Adelaide', 'Brisbane', 'Canberra', 'Darwin', 'Hobart', 'Melbourne', 'Perth (WA)', 'Sydney']
    for city in city_lst:
        db = find_or_create_db(server, city.lower().replace(' ', ''))
        create_view_all(db)
        create_view_covid(db)
