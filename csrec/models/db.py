# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

#if request.env.web2py_runtime_gae:            # if running on Google App Engine
#    db = DAL('gae://mynamespace')             # connect to Google BigTable
#    session.connect(request, response, db = db) # and store sessions and tickets there
#    ### or use the following lines to store sessions in Memcache
#    # from gluon.contrib.memdb import MEMDB
#    # from google.appengine.api.memcache import Client
#    # session.connect(request, response, db = MEMDB(Client()))
#else:                                         # else use a normal relational database
import os.path

# TEST_ENV = os.path.exists("/Users/angleto/test.txt")
#
# if TEST_ENV :
# 	db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
# else:
# 	#import MySQLdb
# 	#from gluon.dal import MySQLAdapter
# 	#MySQLAdapter.driver=MySQLdb
# 	db = DAL('mysql://web2py:Pohfa2ie@localhost/web2py', pool_size=10) # wait_timeout = -1
TEST_ENV=False
db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB

session.connect(request, response, db=db, masterapp='csrec')

## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################
from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

#auth.settings.hmac_key = '<your secret key>'   # before define_tables()
auth.define_tables()                           # creates all needed tables

auth.settings.allow_basic_login = True
auth.settings.actions_disabled.append('register')

auth.settings.login_captcha = False
auth.settings.register_captcha = None
auth.settings.retrieve_username_captcha = None
auth.settings.retrieve_password_captcha = None

auth.settings.expiration = 3600  # seconds


#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled=['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = auth   # auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
