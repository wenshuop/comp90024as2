#encoding:utf-8
import os

from flask import Flask, jsonify, request, render_template
import simplejson as json
import flaskext.couchdb

app = Flask(__name__)

active_users_view = flaskext.couchdb.ViewDefinition('demo', 'active', '''\
function (doc) {
  emit(doc.name, doc.value);
}''')

@app.route('/')
def index():  # put application's code here
    docs = []
    for row in active_users_view():
        docs.append({'name': row.key, 'value': row.value})
    return render_template('route_one.html', docs=json.dumps(docs))


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        COUCHDB_SERVER='http://admin:123456@localhost:5984/',
        COUCHDB_DATABASE='demo'
    )
    # set up couchdb
    manager = flaskext.couchdb.CouchDBManager()
    manager.setup(app)
    # Install the view
    manager.add_viewdef(active_users_view)
    app.run(host='0.0.0.0', port=8090)