
def _get_bases(typ):
    if "__orig_bases__" in getattr(typ, "__dict__", {}):
        # For generic types (see PEP 560)
        # Note that simply checking `hasattr(typ, '__orig_bases__')` is not
        # correct.  Subclasses of a fully-parameterized generic class does not
        # have `__orig_bases__` defined, but `hasattr(typ, '__orig_bases__')`
        # will return True because it's defined in the base class.
        bases_attr = "__orig_bases__"
    else:
        # For regular class objects
        bases_attr = "__bases__"
    return getattr(typ, bases_attr)

