#coding: utf-8

import sys
import os
import time
import tornado
from tornado.options import define, options

ENV = "dev"  #"dev" or "pro"
ROOT = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(ROOT, 'lib/'))

define("port", default=8000, help="listen port", type=int)
define("address", default="127.0.0.1", help="listen address")
tornado.options.parse_command_line()

settings = {}
if ENV == "dev":
    settings["autoreload"] = True

settings["app_root"] = ROOT

settings["template_path"] = "templates/"
settings["data_path"] = "data/"

settings["init_key"] = 'JvBI3SsQtNuH3cwgMcEy5rnICgY7bi4D'
settings["init_file"] = '/var/ansible/tools/init.sh'

settings["redis_host"] = '127.0.0.1'
settings["redis_port"] = 6379


