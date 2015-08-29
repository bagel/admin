from handlers.base import BaseHandler, InitHandler
from handlers.test import TestHandler
from handlers.user import LoginHandler

url_patterns = [
    (r"/", BaseHandler),
    (r"/init", InitHandler),
    (r"/test", TestHandler),
    (r"/login", LoginHandler),
]
