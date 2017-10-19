# -*- coding: utf-8 -*-
import datetime
import uuid

from duffy.database import db, Duffyv1Model
from duffy.extensions import marshmallow
from marshmallow import post_dump

class Project(Duffyv1Model):
    """"""
    __tablename__ = 'users'
    apikey = db.Column(db.String, primary_key=True)
    projectname = db.Column(db.String)
    jobname = db.Column(db.String)
    createdat = db.Column(db.DateTime)
    limitnodes = db.Column(db.Integer)


class Host(Duffyv1Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String)
    ip = db.Column(db.String)
    chassis = db.Column(db.String)
    used_count = db.Column(db.Integer)
    state = db.Column(db.String)
    comment = db.Column(db.String)
    distro = db.Column(db.String)
    rel = db.Column(db.String)
    ver = db.Column(db.String)
    arch = db.Column(db.String)
    pool = db.Column(db.Integer)
    console_port = db.Column(db.Integer)


class HostSchema(marshmallow.ModelSchema):
    @post_dump(pass_many=True)
    def wrap(self, data, many):
        return {'hosts': data}

    class Meta:
        model = Host

session_host_table = db.Table('session_hosts', db.metadata,
                           db.Column('ssid', db.String, db.ForeignKey('sessions.id')),
                           db.Column('hostid', db.String, db.ForeignKey('stock.id')),
                           )


class Session(Duffyv1Model):
    __tablename__ = 'sessions'
    id = db.Column(db.String, default=lambda: str(uuid.uuid4())[:8], primary_key=True)
    delivered_at = db.Column(db.DateTime, default=datetime.datetime.now())
    dropped_at = db.Column(db.DateTime)
    apikey = db.Column(db.String)
    state = db.Column(db.String, default='Deployed')
    jobid = db.Column(db.String)
    hosts = db.relationship('Host', secondary=session_host_table)
