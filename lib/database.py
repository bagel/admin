#coding: utf-8

import os
import sys
import time
import cPickle
import fcntl


class DBPickle(object):
    def __init__(self, dbpath, dbfile):
        self.dbpath = dbpath
        self.dbfile = dbfile
        self._file = os.path.join(self.dbpath, self.dbfile)
        self._fp = open(self._file, 'rb')
        self._lock()

    def __enter__(self):
        pass

    def _lock(self):
        return fcntl.flock(self._fp.fileno(), fcntl.LOCK_EX)

    def _unlock(self):
        return fcntl.flock(self._fp.fileno(), fcntl.LOCK_UN)

    def _read(self):
        self._fp.close()
        self._fp = open(self._file, 'rb')

    def _write(self):
        self._fp.close()
        self._fp = open(self._file, 'wb')

    def _seek(self):
        self._fp.seek(0, 0)

    def _load(self):
        self._seek()
        data = self._fp.read() or {}
        if not data:
            return None
        return cPickle.loads(data)

    def _dump(self, obj):
        return cPickle.dump(obj, self._fp)

    def get(self, key):
        data = self._load()
        return data.get(key, None)

    def save(self, obj):
        self._write()
        res = self._dump(obj)
        self._read()
        return res

    def set(self, key, value):
        obj = self._load()
        if not obj:
            obj = {}
        obj[key] = value
        return self.save(obj)

    def delete(self, key):
        obj = self._load()
        if not obj:
            obj = {}
        if key in obj:
            obj.remove(key)
        return self.save(obj)

    @property
    def update(self):
        return self.set

    def exists(self, key):
        data = self._load() or {}
        if key in data:
            return True
        return False

    def expire(self, key):
        pass

    def __exit__(self):
        self._unlock()
        self._fp.close()
