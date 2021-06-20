from django.conf import settings
from django.core.cache import caches

cache = caches["default"]


def set(key, data, duration, *args, **kwargs):
    cache.set(
        "%s_%s" % (settings.CACHE_PREFIX, key.format(*args, **kwargs)), data, duration
    )


def get(key, *args, **kwargs):
    return cache.get("%s_%s" % (settings.CACHE_PREFIX, key.format(*args, **kwargs)))


def delete(key, *args, **kwargs):
    return cache.delete("%s_%s" % (settings.CACHE_PREFIX, key.format(*args, **kwargs)))


def bulk_get(keys):
    return cache.get_many(keys)


def bulk_delete(keys):
    return cache.delete_many(keys)


def incr(key, delta=1, *args, **kwargs):
    cache.incr(
        "%s_%s" % (settings.CACHE_PREFIX, key.format(*args, **kwargs)), delta=delta
    )


def decr(key, delta=1, *args, **kwargs):
    cache.decr(
        "%s_%s" % (settings.CACHE_PREFIX, key.format(*args, **kwargs)), delta=delta
    )


def get_key(key, *args, **kwargs):
    return "%s_%s" % (settings.CACHE_PREFIX, key.format(*args, **kwargs))


def has_key(key, *args, **kwargs):
    return cache.has_key("%s_%s" % (settings.CACHE_PREFIX, key.format(*args, **kwargs)))


def get_keys_from_prefix(key, *args, **kwargs):
    return cache.keys("%s_%s*" % (settings.CACHE_PREFIX, key.format(*args, **kwargs)))
