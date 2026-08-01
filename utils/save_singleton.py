
def save_singleton(pickler, obj):
    logger.trace(pickler, "Si: %s", obj)
    pickler.save_reduce(_eval_repr, (obj.__repr__(),), obj=obj)
    logger.trace(pickler, "# Si")
    return

