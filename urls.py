from handlers.base import BaseHandler, InitHandler
from handlers.test import TestHandler

url_patterns = [
    (r"/", BaseHandler),
    (r"/init", InitHandler),
    (r"/test", TestHandler),
]
