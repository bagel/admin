#coding: utf-8

import sys
import os
import logging
import time
import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.log
from tornado.options import define, options
from jinja2 import Environment, PackageLoader, FileSystemLoader


class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello World!")

    def render_template(self, template_name, **kwargs):
        env = Environment(loader=FileSystemLoader(self.settings["template_path"]))
        template = env.get_template(template_name)
        return template.render(kwargs)

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

        
