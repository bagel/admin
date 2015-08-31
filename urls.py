from handlers.base import BaseHandler, InitHandler
from handlers.test import TestHandler
from handlers.user import LoginHandler, LogoutHandler, UserHandler

url_patterns = [
    (r"/", BaseHandler),
    (r"/init", InitHandler),
    (r"/test", TestHandler),
    (r"/login", LoginHandler),
    (r"/user", UserHandler),
    (r"/logout", LogoutHandler),
]
