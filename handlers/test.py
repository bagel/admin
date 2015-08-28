#coding: utf-8

import sys
import os
from base import BaseHandler


class TestHandler(BaseHandler):
    def get(self):
        kwargs = {"test": "hello world"}
        self.write(self.render_template("test.j2", **kwargs))
