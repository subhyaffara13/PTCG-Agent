
def _property_reduce(obj):
    return property, (obj.fget, obj.fset, obj.fdel, obj.__doc__)

