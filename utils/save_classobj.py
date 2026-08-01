
def save_classobj(pickler, obj): #FIXME: enable pickler._byref
    if not _locate_function(obj, pickler):
        logger.trace(pickler, "C1: %s", obj)
        pickler.save_reduce(ClassType, (obj.__name__, obj.__bases__,
                                        obj.__dict__), obj=obj)
                                       #XXX: or obj.__dict__.copy()), obj=obj) ?
        logger.trace(pickler, "# C1")
    else:
        logger.trace(pickler, "C2: %s", obj)
        name = getattr(obj, '__qualname__', getattr(obj, '__name__', None))
        StockPickler.save_global(pickler, obj, name=name)
        logger.trace(pickler, "# C2")
    return

