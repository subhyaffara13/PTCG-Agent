
def save_generic_alias(pickler, obj):
    args = obj.__args__
    if type(obj.__reduce__()) is str:
        logger.trace(pickler, "Ga0: %s", obj)
        StockPickler.save_global(pickler, obj, name=obj.__reduce__())
        logger.trace(pickler, "# Ga0")
    elif obj.__origin__ is tuple and (not args or args == ((),)):
        logger.trace(pickler, "Ga1: %s", obj)
        pickler.save_reduce(_create_typing_tuple, (args,), obj=obj)
        logger.trace(pickler, "# Ga1")
    else:
        logger.trace(pickler, "Ga2: %s", obj)
        StockPickler.save_reduce(pickler, *obj.__reduce__(), obj=obj)
        logger.trace(pickler, "# Ga2")
    return

