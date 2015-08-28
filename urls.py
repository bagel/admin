from handlers.base import BaseHandler, InitHandler

url_patterns = [
    (r"/", BaseHandler),
    (r"/init", InitHandler),
]
