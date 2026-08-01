
def save_super(pickler, obj):
    logger.trace(pickler, "Su: %s", obj)
    pickler.save_reduce(super, (obj.__thisclass__, obj.__self__), obj=obj)
    logger.trace(pickler, "# Su")
    return

