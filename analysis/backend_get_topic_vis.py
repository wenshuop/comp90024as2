import couchdb
import pandas as pd
import pyLDAvis
import pyLDAvis.sklearn
from pyLDAvis import PreparedData

def backend_get_topic_vis(db, city, year, month, type):
    # set document id, e.g. 'darwin_2021-01_covid'
    time = str(year) + '-' + '{0:02d}'.format(month)
    doc_id = '{}_{}_{}'.format(city.lower().replace(' ', ''), time, type)

    topic_vis = dict(db.get(doc_id))
    if topic_vis is not None:
        # drop '_id' and '_rev' from the retrieved dictionary
        topic_vis.pop('_id', None)
        topic_vis.pop('_rev', None)
        vis = prepared_data_from_dict(topic_vis)
        pyLDAvis.save_html(vis, '{}_topic_vis.html'.format(doc_id))
    else:
        print('document does not exit.')

def prepared_data_from_dict(vis_data):
    topic_coordinates = pd.DataFrame.from_dict(vis_data['mdsDat'])
    topic_info = pd.DataFrame.from_dict(vis_data['tinfo'])
    token_table = pd.DataFrame.from_dict(vis_data['token.table'])
    R = vis_data['R']
    lambda_step = vis_data['lambda.step']
    plot_opts = vis_data['plot.opts']
    client_topic_order = vis_data['topic.order']
    return PreparedData(topic_coordinates, topic_info,
                        token_table, R, lambda_step, plot_opts, client_topic_order)


if __name__ == '__main__':
    server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')
    db = server['topic_vis']

    # set parameters
    city = 'Melbourne'
    year = 2021
    month = 1
    type = 'covid'

    backend_get_topic_vis(db, city, year, month, type)