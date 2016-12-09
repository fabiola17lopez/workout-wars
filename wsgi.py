#! /usr/bin/env python
from django.core.handlers.wsgi import WSGIHandler

import pinax.env

#---------
import os
import sys

# sys.path.append('/sites/piequeens/')
# sys.path.append('/sites/piequeens/ENV')
#---------

# setup the environment for Django and Pinax
pinax.env.setup_environ(__file__)

# set application for WSGI processing
application = WSGIHandler()
