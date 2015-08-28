#!/usr/bin/env python
#coding: utf-8

import sys
import os
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from settings import settings
from urls import url_patterns

def main():
    application = tornado.web.Application(url_patterns, **settings)
    application.listen(options.port, options.address)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
