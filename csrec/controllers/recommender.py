__author__ = 'angleto'

"""
Update (or insert) item. The unique_id must be given as param
e.g.:
curl -X POST -H "Content-Type: application/json" -d '[{ "_id" : "123", "type": "lady", "category" : "romance"}, { "_id" : "Book1", "type": "male", "category" : "hardcore"}]' 'http://localhost:8000/csrec/recommender/insertitems?unique_id=_id'
"""
@auth.requires_login()
@request.restful()
def insertitems():
    response.headers['Content-Type'] = 'application/json'

    def POST(*args, **kwargs):
        items = json.loads(request.body.read())
        item_id = kwargs['unique_id']
        for i in items:
            engine.db.insert_item(item_id=i[item_id], attributes=i)
    return locals()

"""
e.g.:
curl -X POST -H "Content-Type: application/json" -d '{ "item_info" : ["type", "category"]}' 'http://localhost:8000/csrec/recommender/itemaction?item=item1&user=User1&code=1&only_info=false'
curl -X POST -H "Content-Type: application/json" -d '{ "item_info" : ["type", "category"]}' 'http://localhost:8000/csrec/recommender/itemaction?item=item2&user=User1&code=2&only_info=false'
"""
@auth.requires_login()
@request.restful()
def itemaction():
    response.headers['Content-Type'] = 'application/json'

    def POST(*args, **kwargs):
        only_info = False
        if 'only_info' in kwargs:
            only_info_param = kwargs['only_info']
            if only_info_param.lower() == 'true':
                only_info = True

        try:
            user_id = kwargs['user']
            item_id = kwargs['item']
            code = float(kwargs['code'])
            if 'item_info' in kwargs:
                item_meaningful_info = kwargs['item_info']
            else:
                item_meaningful_info = None
        except KeyError:
            raise HTTP(400, "invalid function call, check parameters")

        engine.db.insert_item_action(
            user_id=user_id,
            item_id=item_id,
            code=code,
            item_meaningful_info=item_meaningful_info,
            only_info=only_info
        )
    return locals()

"""
e.g.:
curl -X POST  'http://localhost:8000/csrec/recommender/socialaction?user=User1&user_to=User2&code=4'
"""
@auth.requires_login()
@request.restful()
def socialaction():
    response.headers['Content-Type'] = 'application/json'

    def POST(*args, **kwargs):
        engine.db.insert_social_action(
            user_id=kwargs['user'],
            user_id_to=kwargs['user_to'],
            code=float(kwargs['code'])
        )
    return locals()

"""
curl -X GET  'http://localhost:8000/csrec/recommender/item?item=Book1'
"""
@auth.requires_login()
@request.restful()
def item():
    response.headers['Content-Type'] = 'application/json'

    def GET(*args, **kwargs):
        item_id = kwargs.get('item')
        item_record = engine.db.get_items(item_id=item_id)
        return json.dumps(item_record)
    return locals()

"""
curl -X GET  'http://localhost:8000/csrec/recommender/recommend?user=User1&limit=10&fast=false'
"""
@auth.requires_login()
@request.restful()
def recommend():
    response.headers['Content-Type'] = 'application/json'

    def GET(*args, **kwargs):
        user = kwargs['user']
        max_recs = int(kwargs.get('limit', 10))
        fast = kwargs.get('fast', False)
        recomms = engine.get_recommendations(user, max_recs=max_recs, fast=fast)
        return json.dumps(recomms)
    return locals()

"""
curl -X POST 'http://localhost:8000/csrec/recommender/reconcile?user_old=User1&user_new=User2'
"""
@auth.requires_login()
@request.restful()
def reconcile():
    response.headers['Content-Type'] = 'application/json'

    def POST(*args, **kwargs):
        old_user_id = kwargs['user_old']
        new_user_id = kwargs['user_new']
        try:
            engine.db.reconcile_user(
                old_user_id=old_user_id,
                new_user_id=new_user_id
            )
        except csrec_exc.MergeEntitiesException as e:
            logger.warn("No reconciliation: %s" % e)
    return locals()

"""
curl -X GET 'http://localhost:8000/csrec/recommender/info/user?user=User1'
curl -X GET 'http://localhost:8000/csrec/recommender/info/item?item=item1'
"""
@auth.requires_login()
@request.restful()
def info():
    response.headers['Content-Type'] = 'application/json'

    def GET(*args, **kwargs):
        if args:
            if args[0] == 'user':
                user_id = kwargs.get('user', '')
                if user_id:
                    item_actions = engine.db.get_item_actions(user_id=user_id)
                    if item_actions:
                        social_actions = engine.db.get_social_actions(user_id=user_id)
                        actions = {'social': social_actions, 'item': item_actions}
                    else:
                        actions = {}
                    return json.dumps(actions)
            if args[0] == 'item':
                    item_id = kwargs.get('item', '')
                    actions_on_items = engine.db.get_item_ratings(item_id=item_id)
                    return json.dumps(actions_on_items)
    return locals()


#TODO: POST http://localhost:8000/csrec/recommender/update/{uid}/profiling/{item_id}
#TODO: GET http://localhost:8000/csrec/recommender/ranking/users/{type}
#TODO: GET http://localhost:8000/csrec/recommender/ranking/items/{type}
#TODO: GET http://localhost:8000/csrec/recommender/query?item_id=X&category=Y
