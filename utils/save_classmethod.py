
def save_classmethod(pickler, obj):
    logger.trace(pickler, "Cm: %s", obj)
    orig_func = obj.__func__

    # if type(obj.__dict__) is dict:
    #     if obj.__dict__:
    #         state = obj.__dict__
    #     else:
    #         state = None
    # else:
    #     state = (None, {'__dict__', obj.__dict__})

    pickler.save_reduce(type(obj), (orig_func,), obj=obj)
    logger.trace(pickler, "# Cm")

