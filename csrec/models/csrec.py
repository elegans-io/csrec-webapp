__author__ = 'angleto'

import logging
logger = logging.getLogger("web2py.app.myapp")
logger.setLevel(logging.WARN)

import json
import csrec

from csrec import Recommender
import csrec.exceptions as csrec_exc

engine = Recommender(dal_name='mem', log_level=True)

