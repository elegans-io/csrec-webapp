__author__ = 'angleto'

import json
import csrec
from csrec import Recommender
from csrec import DALFactory

csrec_db = DALFactory(name='mem', params={})  # instantiate an in memory database
engine = Recommender(csrec_db, log_level=True)

