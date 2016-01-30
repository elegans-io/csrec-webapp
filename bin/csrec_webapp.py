#!/usr/bin/env python
# -*- coding: utf8 -*-

import tornado.httpserver
import tornado.web


from tornado.options import define, options
from tornado.ioloop import IOLoop
import json

from csrec import Recommender
import csrec.exceptions as csrec_exc


define("port", default=8888, help="run on the given port", type=int)


class InsertItemHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.engine = self.application.engine

    """
    Update (or insert) item. The unique_id must be given as param
    e.g.:
    curl -X POST -H "Content-Type: application/json" -d '[{ "_id" : "123", "type": "lady", "category" : "romance"}, { "_id" : "Book1", "type": "male", "category" : "hardcore"}]' 'http://localhost:8000/insertitems?unique_id=_id'
    """
    def post(self):
        try:
            items = json.loads(self.request.body.decode('utf-8'))
        except ValueError:
            raise tornado.web.HTTPError(404, reason="invalid function call, check parameters")

        item_id = self.get_argument("unique_id", default='_id')
        for i in items:
            self.engine.db.insert_item(item_id=i[item_id], attributes=i)
        return self.write(json.dumps({}))


class ItemActionHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.engine = self.application.engine

    """
    e.g.:
    curl -X POST -H "Content-Type: application/json" -d '{ "item_info" : ["type", "category"]}' 'http://localhost:8000/itemaction?item=item1&user=User1&code=1&only_info=false'
    curl -X POST -H "Content-Type: application/json" -d '{ "item_info" : ["type", "category"]}' 'http://localhost:8000/itemaction?item=item2&user=User1&code=2&only_info=false'
    """
    def post(self):
        only_info_p = self.get_argument("only_info", default='false')
        if only_info_p == 'true':
            only_info = True
        else:
            only_info = False

        try:
            user_id = self.get_argument("user")
            item_id = self.get_argument("user")
            code = float(self.get_argument("code"))
        except:
            raise tornado.web.HTTPError(404, reason="invalid function call, check parameters")

        try:
            item_meaningful_info = json.loads(self.request.body.decode('utf-8'))
        except ValueError:
            item_meaningful_info = {}

        self.engine.db.insert_item_action(
            user_id=user_id,
            item_id=item_id,
            code=code,
            item_meaningful_info=item_meaningful_info,
            only_info=only_info
        )
        return self.write(json.dumps({}))


class SocialActionHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.engine = self.application.engine

    """
    e.g.:
    curl -X POST  'http://localhost:8000/socialaction?user=User1&user_to=User2&code=4'
    """
    def post(self):
        try:
            user_id = self.get_argument("user")
            user_id_to = self.get_argument("user_to")
            code = float(self.get_argument("code"))
        except:
            raise tornado.web.HTTPError(404, reason="invalid function call, check parameters")

        self.engine.db.insert_social_action(
            user_id=user_id,
            user_id_to=user_id_to,
            code=code)
        return self.write(json.dumps({}))

class ItemHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.engine = self.application.engine

    """
    curl -X GET  'http://localhost:8000/item?item=Book1'
    """
    def get(self):
        try:
            item_id = self.get_argument("item")
        except:
            raise tornado.web.HTTPError(404, reason="invalid function call, check parameters")

        item_record = self.engine.db.get_items(item_id=item_id)
        return self.write(json.dumps(item_record))


class RecommendHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.engine = self.application.engine

    """
    curl -X GET  'http://localhost:8000/recommend?user=User1&limit=10&fast=false'
    """
    def get(self):
        try:
            user = self.get_argument("user")
        except:
            raise tornado.web.HTTPError(404, reason="invalid function call, check parameters")

        fast_p = self.get_argument("fast", default='false')
        if fast_p == 'true':
            fast = True
        else:
            fast = False

        limit = int(self.get_argument("limit", default=10))

        recomms = self.engine.get_recommendations(user, max_recs=limit, fast=fast)
        return self.write(json.dumps(recomms))


class ReconcileHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.engine = self.application.engine

    """
    curl -X POST 'http://localhost:8000/reconcile?user_old=User1&user_new=User2'
    """
    def post(self):
        try:
            old_user_id = self.get_argument("user_old")
            new_user_id = self.get_argument("user_new")
        except:
            raise tornado.web.HTTPError(404, reason="invalid function call, check parameters")

        try:
            self.engine.db.reconcile_user(
                old_user_id=old_user_id,
                new_user_id=new_user_id
            )
        except csrec_exc.MergeEntitiesException as e:
            raise tornado.web.HTTPError(404, reason="unable to reconcile users: " + e)
        return self.write(json.dumps({}))


class InfoUserHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.engine = self.application.engine

    """
    curl -X GET 'http://localhost:8000/info/user?user=User1'
    """
    def get(self):
        try:
            user_id = self.get_argument("user")
        except:
            raise tornado.web.HTTPError(404, reason="invalid function call, check parameters")

        item_actions = self.engine.db.get_item_actions(user_id=user_id)
        if item_actions:
            social_actions = self.engine.db.get_social_actions(user_id=user_id)
            actions = {'social': social_actions, 'item': item_actions}
        else:
            actions = {}
        return self.write(json.dumps(actions))


class InfoItemHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.engine = self.application.engine

    """
    curl -X GET 'http://localhost:8000/info/user?user=User1'
    """
    def get(self):
        try:
            item_id = self.get_argument("item")
        except:
            raise tornado.web.HTTPError(404, reason="invalid function call, check parameters")

        actions_on_items = self.engine.db.get_item_ratings(item_id=item_id)
        return self.write(json.dumps(actions_on_items))


class SerializeHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.engine = self.application.engine

    """
    curl -X GET 'http://localhost:8000/serialize?filename=/tmp/dump.bin'
    """
    def get(self):
        try:
            filename = self.get_argument("filename", "dump.bin")
        except:
            raise tornado.web.HTTPError(404, reason="invalid function call, check parameters")

        self.engine.db.serialize(filepath=filename)

        try:
            self.engine.db.serialize(filepath=filename)
        except csrec_exc.SerializeException:
            raise tornado.web.HTTPError(404, reason="serialization error")

        return self.write(json.dumps({}))


class RestoreHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        tornado.web.RequestHandler.__init__(self, *args, **kwargs)
        self.engine = self.application.engine

    """
    curl -X GET 'http://localhost:8000/restore?filename=/tmp/dump.bin'
    """
    def get(self):
        try:
            filename = self.get_argument("filename", "dump.bin")
        except:
            raise tornado.web.HTTPError(404, reason="invalid function call, check parameters")

        self.engine.db.restore(filepath=filename)

        try:
            self.engine.db.restore(filepath=filename)
        except csrec_exc.RestoreException:
            raise tornado.web.HTTPError(404, reason="restore error")

        return self.write(json.dumps({}))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/insertitems", InsertItemHandler),
            (r"/itemaction", ItemActionHandler),
            (r"/socialaction", SocialActionHandler),
            (r"/item", ItemHandler),
            (r"/recommend", RecommendHandler),
            (r"/reconcile", ReconcileHandler),
            (r"/info/item", InfoItemHandler),
            (r"/info/user", InfoUserHandler),
            (r"/serialize", SerializeHandler),
            (r"/restore", RestoreHandler),
            ]

        settings = dict(
        )

        self.engine = Recommender(dal_name='mem', log_level=True)
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    application = Application()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()

