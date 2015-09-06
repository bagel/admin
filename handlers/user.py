#coding: utf-8

import os
import sys
import random
import time
import hashlib
import base64
import json
import string
import qrcode
import qrcode.image.svg
import cStringIO
from base import BaseHandler
from database import DBPickle
from ldaplib import LDAP


class UserHandler(BaseHandler):
    def initialize(self):
        self.dbp = DBPickle(self.settings["data_path"], "user.pke")
        self.ldap = LDAP(self.settings["ldap_url"],
                         self.settings["ldap_secret"],
                         self.settings["ldap_dn"],
                         self.settings["ldap_ou"])

    def _redirect(self):
        self.clear_cookie("CK_token")
        self.redirect("/login")

    def qrcode_svg(self, user, secret):
        fp = cStringIO.StringIO()
        s = 'otpauth://totp/{}@tunnel01?secret={}&issuer=tunnel01'
        qr = qrcode.make(s.format(user, secret), image_factory=qrcode.image.svg.SvgPathImage)
        qr.save(fp)
        svg = fp.getvalue()
        fp.close()
        return svg

    def add_user(self, mail):
        return self.ldap.add(mail)

    def update_ssha(self, mail, passwd):
        return self.ldap.update_ssha(mail, passwd)

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
        kwargs = {"user": user, "qrcode_svg": self.qrcode_svg(user, "GFGFGIK2JFQTGVCA")}
        self.write(self.render_template("user.html", **kwargs))

class UserAddHander(UserHandler):
    def post(self):
        pass

    def get(self):
        pass

class UserUpdateSSHAHandler(UserHandler):
    def get(self):
        pass

    def post(self):
        data = {}
        data["result"] = -1
        user = self.get_body_argument("user", default="")
        if not user:
            data["errmsg"] = "用户名不存在"
            return self.write(json.dumps(data))
        passwd = self.get_body_argument("passwd", default="")
        if not passwd:
            data["errmsg"] = "密码不合法"
            return self.write(json.dumps(data))
        if len(passwd) < 10:
            data["errmsg"] = "密码长度小于10"
            return self.write(json.dumps(data))
        i = j = k = 0
        for p in passwd:
            if p in string.digits:
                i = 1
            if p in string.letters:
                j = 1
            if p not in string.digits + string.letters:
                k = 1
        if i == 0 or j == 0 or k == 0:
            data["errmsg"] = "密码必须包含数字、字母和特殊字符"
            return self.write(json.dumps(data))
        self.update_ssha("{}@changker.com".format(user), passwd)
        data["result"] = 0
        return self.write(json.dumps(data))


class LoginHandler(UserHandler):
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


class LogoutHandler(UserHandler):
    def get(self):
        self._redirect()
