__author__ = 'angleto'

import logging
logger = logging.getLogger("web2py.app.myapp")
logger.setLevel(logging.WARN)

import json
import csrec

from csrec import Recommender
from csrec import factory_dal
import csrec.exceptions as csrec_exc

#csrec_db = factory_dal.Dal.get_dal(name='mem', params={})  # instantiate an in memory database
csrec_db = factory_dal.Dal.get_dal(name='mem', params={})  # instantiate an in memory database
engine = Recommender(csrec_db, log_level=True)

