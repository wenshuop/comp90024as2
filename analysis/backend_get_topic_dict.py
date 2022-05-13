'''
Team 13, Melbourne
Jing Qiu, 1152016, jiqiu1@student.unimelb.edu.au
Meijun Yue, 1190161, meijuny@student.unimelb.edu.au
Suyi Jiao, 1222833, sjjiao@student.unimelb.edu.au
Yeting Wu, 1310061, yetingw@student.unimelb.edu.au
Wenshuo Pan, 1226506, wenshuop@student.unimelb.edu.au
'''

import couchdb
import matplotlib.pyplot as plt


def backend_get_topic_dict(db, city, year, month, type):
    # set document id, e.g. 'darwin_2021-01_covid'
    time = str(year) + '-' + '{0:02d}'.format(month)
    doc_id = '{}_{}_{}'.format(city.lower().replace(' ', ''), time, type)

    topic_dict = dict(db.get(doc_id))
    if topic_dict is not None:
        # drop '_id' and '_rev' from the retrieved dictionary
        topic_dict.pop('_id', None)
        topic_dict.pop('_rev', None)
    else:
        print('document does not exit.')

    # print out the topic dictionary
    plot_top_words(topic_dict, '{}_topic_dict'.format(doc_id), doc_id)


def plot_top_words(topics, title, doc_id):
    fig, axes = plt.subplots(1, 5, figsize=(30, 15), sharex=True)
    axes = axes.flatten()
    for topic_idx, [top_features, weights] in topics.items():
        topic_idx = int(topic_idx)
        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f"Topic {topic_idx +1}", fontdict={"fontsize": 30})
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=20)
        for i in "top right left".split():
            ax.spines[i].set_visible(False)
        fig.suptitle(title, fontsize=40)
    plt.subplots_adjust(top=0.90, bottom=0.05, wspace=0.90, hspace=0.3)
    # plt.show()
    plt.savefig('{}_topic_dict.png'.format(doc_id))


if __name__ == '__main__':
    server = couchdb.Server('http://admin:admin@172.26.128.22:5984//')
    db = server['topic_dict']

    # set parameters
    city = 'Melbourne'
    year = 2021
    month = 1
    type = 'covid'

    backend_get_topic_dict(db, city, year, month, type)