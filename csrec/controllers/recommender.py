__author__ = 'angleto'

"""
Update (or insert) item. The unique_id must be given as param
e.g.:
curl -X POST -H "Content-Type: application/json" -d '[{ "_id" : "123", "type": "lady", "category" : "romance"}, { "_id" : "Book1", "type": "male", "category" : "hardcore"}]' 'http://localhost:8000/csrec/recommender/insertitems?unique_id=_id'
"""
@auth.requires_login()
@request.restful()
def insertitems():
    response.view = 'generic.json'

    def POST(*args, **vars):
        items = json.loads(self.request.body)
        item_id = self.request.params['unique_id']
        for i in items:
            csrec_db.insert_item(item_id=i[item_id], attributes=i)
    return locals()

"""
e.g.:
curl -X POST  'http://localhost:8000/csrec/recommender/itemaction?item=Book1&user=User1&code=1&item_info=my_category&only_info=false'
curl -X POST  'http://localhost:8000/csrec/recommender/itemaction?item=Book2&user=User1&code=2&item_info=my_category&only_info=false'
curl -X POST  'http://localhost:8000/csrec/recommender/itemaction?item=Book3&user=User2&code=3&item_info=my_category&only_info=false'
curl -X POST  'http://localhost:8000/csrec/recommender/itemaction?item=Book4&user=User2&code=4&item_info=my_category&only_info=false'
"""
@auth.requires_login()
@request.restful()
def itemaction():
    response.view = 'generic.json'

    def POST(*args, **vars):
        only_info = kwargs['only_info']
        if only_info.lower() == 'true':
            only_info = True
        else:
            only_info = False
        csrec_db.insert_item_action_recommender(
            user_id=kwargs['user'],
            item_id=kwargs['item'],
            code=float(kwargs['code']),
            item_meaningful_info=kwargs['item_info'],
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
    response.view = 'generic.json'

    def POST(*args,**kwargs):
        csrec_db.insert_social_action(
            user_id=kwargs['user'],
            user_id_to=kwargs['user_to'],
            code=float(kwargs['code'])
        )
    return locals()

"""
curl -X GET  'http://localhost:8000/csrec/recommender/item?id=Book1'
"""
@auth.requires_login()
@request.restful()
def item():
    response.view = 'generic.json'

    def GET(*args, **kwargs):
        item_id = kwargs.get('id')
        item_record = csrec_db.get_item(item_id=item_id)
        return item_record
    return locals()

"""
curl -X GET  'http://localhost:8000/csrec/recommender/recommend?user=User1&max_recs=10&fast=False'
"""
@auth.requires_login()
@request.restful()
def recommend():
    response.view = 'generic.json'

    def GET(*args, **kwargs):
        user = kwargs['user']
        max_recs = int(kwargs.get('max_recs', 10))
        fast = kwargs.get('fast', False)
        recomms = engine.get_recommendations(user, max_recs=max_recs, fast=fast)
        return recomms

"""
curl -X POST 'http://localhost:8000/csrec/recommender/reconcile?old=User1&new=User2'
"""
@auth.requires_login()
@request.restful()
def reconcile():
    response.view = 'generic.json'

    def POST(*args, **kwargs):
        old_user_id = kwargs['old']
        new_user_id = kwargs['new']
        csrec_db.reconcile_user(
            old_user_id=old_user_id,
            new_user_id=new_user_id
        )
    return locals()

"""
curl -X GET  'http://localhost:8000/csrec/recommender/info/user?user=User1'
"""
@auth.requires_login()
@request.restful()
def info():
    response.view = 'generic.json'

    def GET(*args, **kwargs):
        if args and args[0] == 'user':
            if args[0] == 'user':
                user_id = kwargs['user']
                recomms = csrec_db.get_user_item_actions(user_id=user_id)
                return recomms
    return locals()


#TODO: POST http://localhost:8000/csrec/recommender/update/{uid}/profiling/{item_id}
#TODO: GET http://localhost:8000/csrec/recommender/ranking/users/{type}
#TODO: GET http://localhost:8000/csrec/recommender/ranking/items/{type}
#TODO: GET http://localhost:8000/csrec/recommender/info/item/{item_id}
#TODO: GET http://localhost:8000/csrec/recommender/query?item_id=X&category=Y