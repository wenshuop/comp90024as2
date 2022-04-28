#encoding:utf-8
import os
from flask import Flask, jsonify, request, render_template
# import simplejson as json
app = Flask(__name__)
# import models
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pl,kuhb10.@127.0.0.1/fund'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


@app.route('/')
def index():
    return render_template('route_one.html')


if __name__ == '__main__':
    # models.db.init_app(app)
    app.run(host='0.0.0.0', port=5000)
