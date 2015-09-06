import sys
import os
import re
import subprocess
import ldap
import ldap.modlist


LDAP_USER_AUTH_SUCC = 0
LDAP_USER_AUTH_FAIL = 1
LDAP_USER_NOT_FOUND = 2
LDAP_USER_NOT_VALID = 3

class LDAP(object):
    def __init__(self, url, secret, dn, ou):
        self._l = ldap.initialize(url)
        self._secret = secret
        self._dn = dn
        self._ou = ou

    def auth(self, user, passwd):
        if not re.match(r'\w+\@changker.com', user):
            return LDAP_USER_NOT_VALID
        self._l.bind(self._dn, self._secret)
        res = self._l.search_s(self._ou, ldap.SCOPE_SUBTREE, "(mail={})".format(user))
        if not res:
            return LDAP_USER_NOT_FOUND
        dn = res[0][0]
        try:
            if self._l.bind_s(dn, passwd):
                return LDAP_USER_AUTH_SUCC
        except ldap.INVALID_CREDENTIALS:
            pass
        return LDAP_USER_AUTH_FAIL

    def add(self, mail):
        self._l.bind(self._dn, self._secret)
        user = mail.split('@')[0]
        dn = "mail={},{}".format(mail, self._ou)
        attrs = {
            "objectClass": "inetOrgPerson",
            "sn": user,
            "cn": user,
            "mail": mail,
            "userPassword": "{SSHA}",
            "userPassword": "{TOTP}"
        }
        ldif = ldap.modlist.addModlist(attrs)
        self._l.add_s(dn, ldif)
        return

    def update(self, mail, old, new):
        self._l.simple_bind_s(self._dn, self._secret)
        dn = "mail={},{}".format(mail, self._ou)
        print old, new
        ldif = ldap.modlist.modifyModlist(old, new)
        print ldif
        attrs = [
            (ldap.MOD_DELETE, "userPassword", old["userPassword"]),
            (ldap.MOD_ADD, "userPassword", new["userPassword"]),
        ]
        self._l.modify_s(dn, attrs)
        return

    def search(self, mail):
        self._l.bind(self._dn, self._secret)
        res = self._l.search_s(self._ou, ldap.SCOPE_SUBTREE, "(mail={})".format(mail))
        return res

    def update_ssha(self, mail, passwd):
        p = subprocess.Popen('/usr/bin/slappasswd -s "{}"'.format(passwd), shell=True, stdout=subprocess.PIPE)
        p.wait()
        new_passwd = p.stdout.read().strip()
        user_passwd = self.search(mail)[0][1]["userPassword"]
        for passwd in user_passwd:
            if re.match('{SSHA}', passwd):
                old_passwd = passwd
                break
        old = {"userPassword": old_passwd}
        new = {"userPassword": new_passwd}
        return self.update(mail, old, new)

    def update_totp(self, mail):
        tmp_secret = os.tmpnam()
        p = subprocess.Popen('/usr/bin/google-authenticator -q --qr-mode=NONE -d -f -t -r 3 -R 30 -w 17 -s {}'.format(tmp_secret))
        p.wait()
        with open(tmp_secret, "r") as fp:
            new_secret = fp.readline().strip()
        os.unlink(tmp_secret)
        user_secret = self.search(mail)[0][1]["userPassword"]
        for secret in user_secret:
            if re.match('{TOTP}', secret):
                old_secret = secret
                break
        old = {"userPassword": old_secret}
        new = {"userPassword": "{TOTP}" + new_secret}
        return self.update(mail, old, new)

    def delete(self, mail):
        self._l.bind(self._dn, self._secret)
        dn = "mail={},{}".format(mail, self._ou)
        self._l.delete_s(dn)
        return
