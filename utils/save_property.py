
def save_property(pickler, obj):
    logger.trace(pickler, "Pr: %s", obj)
    pickler.save_reduce(type(obj), (obj.fget, obj.fset, obj.fdel, obj.__doc__),
                        obj=obj)
    logger.trace(pickler, "# Pr")

