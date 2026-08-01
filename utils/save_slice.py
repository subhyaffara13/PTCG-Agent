
def save_slice(pickler, obj):
    logger.trace(pickler, "Sl: %s", obj)
    pickler.save_reduce(slice, (obj.start, obj.stop, obj.step), obj=obj)
    logger.trace(pickler, "# Sl")
    return

