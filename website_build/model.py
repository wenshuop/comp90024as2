# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Table
from flask_sqlalchemy import SQLAlchemy
import app

db = SQLAlchemy(app.app)


class Pie(db.Model):
    __tablename__ = 'pie'

    name = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.Integer)