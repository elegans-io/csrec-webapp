*******************************************
A web app to use the cold-start-recommender
*******************************************


This is a basic [web2py](http://www.web2py.com) application provide a web interface to the [cold-start-recommender](https://github.com/elegans-io/cold-start-recommender)

The csrec application is a work in progress and works only with the branch better\_webapp of [cold-start-recommender](https://github.com/elegans-io/cold-start-recommender), further details will be provided soon.

Dependencies
============

The application depende on [web2py](http://www.web2py.com) and [cold-start-recommender](https://github.com/elegans-io/cold-start-recommender)


Installation
============

wget http://www.web2py.com/examples/static/web2py_src.zip

unzip web2py.zip

wget https://github.com/elegans-io/csrec-webapp/archive/master.zip

unzip master.zip

(entering virtualenv)

install csrec

copying application into web2py/applications

./web2py.py --password=password -D 0 --verbose --ip=0.0.0.0