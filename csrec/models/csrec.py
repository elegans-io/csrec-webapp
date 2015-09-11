__author__ = 'angleto'

import json
import csrec

from csrec import Recommender
from csrec import factory_dal

csrec_db = factory_dal.Dal.get_dal(name='mem', params={})  # instantiate an in memory database
engine = Recommender(csrec_db, log_level=True)

