# -*- mode: python; coding: utf-8; -*-
import pylibmc as memcache
from django.core.cache.backends import memcached

import time
from django.core.cache.backends.base import BaseCache
from django.utils.encoding import smart_str

class CacheClass(memcached.CacheClass):
    def init(self, server, params):
        BaseCache.init(self, params)
        #self._cache = memcache.Client(server.split(';'))
        self._cache = memcache.Client(server.split(';'), binary=True)

def _get_memcache_timeout(self, timeout):
    """
    Memcached deals with long (> 30 days) timeouts in a special
    way. Call this function to obtain a safe value for your timeout.
    """
    # Allow infinite timeouts
    if timeout is None:
        timeout = self.default_timeout
    if timeout > 2592000: # 60*60*24*30, 30 days
        # See http://code.google.com/p/memcached/wiki/FAQ
        # "You can set expire times up to 30 days in the future. After that
        # memcached interprets it as a date, and will expire the item after
        # said date. This is a simple (but obscure) mechanic."
        #
        # This means that we have to switch to absolute timestamps.
        timeout += int(time.time())
    return timeout

def add(self, key, value, timeout=None, min_compress_len=150000):
    if isinstance(value, unicode):
        value = value.encode('utf-8')
    return self._cache.add(smart_str(key), value, 
                                    self._get_memcache_timeout(timeout), 
                                    min_compress_len)

def set(self, key, value, timeout=None, min_compress_len=150000):
    if isinstance(value, unicode):
        value = value.encode('utf-8')
    self._cache.set(smart_str(key), value, 
                        self._get_memcache_timeout(timeout), 
                        min_compress_len)