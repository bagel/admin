#coding: utf-8

import sys
import os
import logging
import time
import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.log


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!")

class InitHandler(BaseHandler):
    def post(self):
        key = self.get_body_argument("key", default="")
        if not key or key != self.settings["init_key"]:
            self.write('init key not match')
            return
        if not os.access(self.settings["init_file"], os.R_OK):
            self.write('init file not readable')
        with open(self.settings["init_file"], 'r') as fp:
            self.write(fp.read())

class DnsHandler(BaseHandler):
    def get(self):
        ip = self.get_query_argument("ip", default=None)
        domain = self.get_query_argument("domain", default=None)
