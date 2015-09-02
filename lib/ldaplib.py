import sys
import os
import re
import ldap


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

    def add(self, user):
        pass

