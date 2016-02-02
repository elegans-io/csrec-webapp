*******************************************
A web app to use the cold-start-recommender
*******************************************

This is a basic [tornado](http://www.tornadoweb.org/) application which provide a web interface to the [cold-start-recommender](https://github.com/elegans-io/cold-start-recommender)

# Dependencies

* [tornado](http://www.tornadoweb.org/)
* [cold-start-recommender](https://github.com/elegans-io/cold-start-recommender) version >= 4.0.0

# Installation

pip install csrec-webapp

# Running the application

csrec_webapp.py --port=8888

# APIs

## Item data Input

Items must have at least the following fields:

* A unique identifier. No matter if it is a string or an int, but must be unique.
* A type identifier. The recommender must be able to recognise which type of item is dealing with (program, series, news etc).
* Informative fields. Prior to use, the recommender must know which fields are the informative ones

## User behaviour data input

The application must tell which action is performed by which user on which item.

## Output

For each user, the recommender can recommend different types of items.

Note that:

* The recommender does not consider which programs/series are scheduled for a certain day.
* Items for a certain period must be filtered by the user after the query.
* The recommender can filter the type of items (eg if programs or series or news should be recommended to a certain user), but cannot recommend the informative fields (eg "this user likes running shoes").
* Whenever not enough information is available, the recommender recommends the most popular items.

## Functions

### Update items table

Insert or modify items.

#### methods

POST

#### URL Params

##### Required

* unique_id: the name of the field used as unique id for the item

#### Data Params

A list of items with type and category informations e.g.:

```
[{ "_id" : "item1", "type": "lady", "category" : "high_heels"},
    { "_id" : "item2", "type": "male", "category" : "mocassino"},
    { "_id" : "item3", "type": "unisex", "category" : "mocassino"},
    { "_id" : "item4", "type": "male", "category" : "mocassino"}]
```

#### Success Response

Code: 200

Content: {}

#### Error Response

Code: 404

Content: {}

#### Sample Call

```bash
curl -X POST -H "Content-Type: application/json"  -d '[{ "_id" : "item1", "type": "lady", "category" : "high_heels"}, { "_id" : "item2", "type": "male", "category" : "mocassino"}, { "_id" : "item3", "type": "unisex", "category" : "mocassino"}, { "_id" : "item4", "type": "male", "category" : "mocassino"}]' 'http://elegans.it:8000/insertitems?unique_id=_id'
```

### Post user action on an item

#### methods

POST

#### URL Params

##### Required

* item: the item id (program, series etc)
* user: This could be the value of rating, or could correspond to different actions (e.g. hated: -1, loved: +1)
* code: the rating

##### Optional

* only_info: true or false, default is false

#### Description

Update/insert an action identified by code performed by {uid} on {item_id}. If users or item are not found they are created in the database.

#### Success Response

Code: 200

Content: {}

#### Error Response

Code: 404

Content: {}

#### Sample Call

```bash
curl -X POST  -H "Content-Type: application/json" -d '{ "item_info" : ["type", "category"]}' 'http://elegans.it:8000/itemaction?item=item1&user=User1&code=1&only_info=false'
```

### Post a social action (users to users)

#### methods

POST

#### Description

Stores information about action performed by {uid} on {other_uid}, like "follow", "like" etc. If id's are not found they are created in the database.

#### URL Params

##### Required

* user: email or session_id of the user. NB Always use email if available.
* code: This could be the liking factor, or could correspond to different actions (e.g. downvote: -1, follow: +1)
* user_to: the other user's id

#### Success Response

Code: 200

Content: {}

#### Error Response

Code: 404

Content: {}

#### Sample Call

```bash
curl -X POST 'http://elegans.it:8000/socialaction?user=User1&user_to=User2&code=3'
```

### Get recommended items for a user

#### methods

GET

#### Description

Provide a list of recommended item_ids.

#### URL Params

##### Required

* user: email or session_id of the user. NB Always use email if available.

##### Optional

* fast: if set to any value, uses faster and less accurate algorithm
* limit: integer, number of items to return, default is 10
* type: type of items to be returned. NB: if a non-existent key is provided the recommender will return an empty list

#### Success Response

Code: 200

Content: a list of items e.g.: ```["item4", "item1", "item3", "item2", "User2"]```

#### Error Response

Code: 404

Content: {}

#### Sample Call

```bash
curl -X GET 'http://elegans.it:8000/recommend?user=User1&limit=10'
```

### Reconcile session_id with user ID

#### methods

POST

#### Description

Whenever a user logs in not in the first session, the app should tell which session_id s/he was using during the previous sessions. All action associated to user_old will be associated to user_new.

#### URL Params

##### Required

* user_old: old user id
* user_new: new user id

#### Success Response

Code: 200

Content: {}

#### Error Response

Code: 404

Content: {}

#### Sample Call

```bash
curl -X POST 'http://elegans.it:8000/reconcile?user_old=User1&user_new=User2
```

### Get action of a user

#### methods

GET

#### Description

Return a dictionary with two lists:

#### URL Params

* itemaction: actions performed on items
* socialaction: actions performed on other users

#### URL Params

##### Required

* user: email or session_id of the user. NB Always use email if available..

#### Success Response

Code: 200

Content: {}

#### Error Response

Code: 404

Content: {}

#### Sample Call

```bash
curl -X GET 'http://elegans.it:8000/info/user?user=User1'
```

### Get interactions on an item

#### methods

GET

#### Description

List of user who performed any action on the item, and which action

#### URL Params

##### Required

* item: id of the item

#### Success Response

Code: 200

Content: {}

#### Error Response

Code: 404

Content: {}

#### Sample Call

```bash
curl -X GET 'http://localhost:8000/info/item?item=item1'
```

### Serialize the data on files

#### methods

GET

#### Description

serialize data on file

#### URL Params

##### Optional

* filename: the path where to serialize the data, default is /tmp/dump.bin

#### Success Response

Code: 200

Content: {}

#### Error Response

Code: 404

Content: {}

#### Sample Call

```bash
curl -X GET 'http://localhost:8000/serialize?filename=/tmp/dump.bin'
```

### Restore data from file
 
#### methods

GET

#### Description

restore data from file

#### URL Params

##### Optional

* filename: the path of the file which contains the serialized data

#### Success Response

Code: 200

Content: {}

#### Error Response

Code: 404

Content: {}

#### Sample Call

```bash
curl -X GET 'http://localhost:8000/restore?filename=/tmp/dump.bin'
```
