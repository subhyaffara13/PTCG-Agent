from typing import Callable

def cached_property(func: Callable) -> property:
    cached_name = f"_cached_{func}"
    sentinel = object()

    def inner(instance: object):
        cache = getattr(instance, cached_name, sentinel)
        if cache is not sentinel:
            return cache
        result = func(instance)
        setattr(instance, cached_name, result)
        return result

    return property(inner)


def cached_property(func):
    '''Decorator to cache property method'''
    attrname = '__' + func.__name__
    _cached_property_sentinel = object()
    def propfunc(self):
        val = getattr(self, attrname, _cached_property_sentinel)
        if val is _cached_property_sentinel:
            val = func(self)
            setattr(self, attrname, val)
        return val
    return property(propfunc)

