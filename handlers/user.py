#coding: utf-8

import os
import sys
import random
from base import BaseHandler
from database import DBPickle


class LoginHandler(BaseHandler):
    def initialize(self):
        self.dbp = DBPickle(self.settings["data_path"], "user.pke")

    def get(self):
        self.dbp.set("test", "hello world {}".format(random.randint(1, 100000)))
        if not self.dbp.exists("user"):
            self.dbp.set("user", 'caoyu{}'.format(random.randint(1, 10)))
        kwargs = {"test": self.dbp.get("test"), "user": self.dbp.get("user")}
        self.write(self.render_template("login.html", **kwargs))
