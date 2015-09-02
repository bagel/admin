#coding: utf-8

import os
import sys
import random
import time
import hashlib
import base64
from base import BaseHandler
from database import DBPickle
from ldaplib import LDAP


class LoginHandler(BaseHandler):
    def initialize(self):
        self.dbp = DBPickle(self.settings["data_path"], "user.pke")
        self.ldap = LDAP(self.settings["ldap_url"],
                         self.settings["ldap_secret"],
                         self.settings["ldap_dn"],
                         self.settings["ldap_ou"])

    def get(self):
        self.clear_cookie("CK_token")
        self.write(self.render_template("login.html"))

    def post(self):
        mail = self.get_body_argument("mail", default="")
        password = self.get_body_argument("password", default="")
        errmsg = ""
        res = -1
        if not mail or not password:
            errmsg = "用户名或密码输入不合法"
        else:
            res = self.ldap.auth(mail, password)
            if res == 1:
                errmsg = "认证失败，用户名或密码错误"
            elif res == 2:
                errmsg = "用户名不存在"
            elif res == 3:
                errmsg = "用户名不合法"
            elif res != 0:
                errmsg = "未知错误"
        if res == 0 and not errmsg:
            tm = int(time.time()) / 3600
            user = mail.split('@')[0]
            h = hashlib.md5("{}#{}#CK".format(user, tm)).hexdigest()[:10]
            v = base64.b64encode("{}.{}".format(user, h))
            self.set_cookie("CK_token", v)
            self.redirect("/user")
            return
        kwargs = {"errmsg": errmsg.decode('utf-8')}
        self.write(self.render_template("login.html", **kwargs))


class UserHandler(BaseHandler):
    def _redirect(self):
        self.clear_cookie("CK_token")
        self.redirect("/login")

    def get(self):
        token = self.get_cookie("CK_token", default="")
        if not token:
            return self._redirect()
        try:
            token = base64.b64decode(token)
            user, h = token.split('.')
        except:
            return self._redirect()
        tm = int(time.time()) / 3600
        if h != hashlib.md5("{}#{}#CK".format(user, tm)).hexdigest()[:10]:
            return self._redirect()
        kwargs = {"user": user}
        self.write(self.render_template("user.html", **kwargs))


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("CK_token")
        self.redirect("/login")
