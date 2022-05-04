#encoding:utf-8
# 导入Flask类库
import os

from flask import Flask, jsonify, request, render_template
import simplejson as json
#import flaskext.couchdb

# 创建应用实例
app = Flask(__name__)
# 在app创建以后才能引入数据库文件
# import model


# # 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名test
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pl,kuhb10.@127.0.0.1/twitter'
# # 设置这一项是每次请求结束后都会自动提交数据库中的变动
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     # models.db.init_app(app)
#     app.run(debug=True)

# docs_by_author = ViewDefinition('docs', 'pie',
#                                 'function(doc) { emit(doc.username, doc);}')

# active_users_view = flaskext.couchdb.ViewDefinition('demo', 'active', '''\
# function (doc) {
#   emit(doc.name, doc.value);
# }''')

# map_func = '''function(doc)
# 	{ emit(doc.doc_rev, doc); }'''
# myQuery = [docType].query(db, map_func, reduce_fun=None)


#@app.route('/')
#def index():  # put application's code here
    # return 'Hello World!'
    # pie = model.Pie.query.all()
    # pies = []
    # for i in pie:
    #     pies.append({
    #         "name": i.name,
    #         "value": i.value,
    #     })
    # print(json.dumps((pies)))
    #docs = []
    #for row in active_users_view():
        #docs.append({'name': row.key, 'value': row.value})
    # return render_template('route_one.html', docs=json.dumps(docs))
    #return render_template('layout.html')

    
@app.route('/')
def layout():  # put application's code here
    return render_template('homepage.html')



if __name__ == '__main__':
    # model.db.init_app(app)
   # app.config.update(
    #    DEBUG=True,
     #   COUCHDB_SERVER='http://admin:123456@localhost:5984/',
    #    COUCHDB_DATABASE='demo'
    #)
    # set up couchdb
    # manager = flaskext.couchdb.CouchDBManager()
    # manager.setup(app)
    # Install the view
    # manager.add_viewdef(active_users_view)
    app.run(host='0.0.0.0', port=8000,debug=True)