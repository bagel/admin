from handlers.main import MainHandler, InitHandler

url_patterns = [
    (r"/", MainHandler),
    (r"/init", InitHandler),
]
