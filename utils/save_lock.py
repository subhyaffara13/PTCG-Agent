
def save_lock(pickler, obj):
    logger.trace(pickler, "Lo: %s", obj)
    pickler.save_reduce(_create_lock, (obj.locked(),), obj=obj)
    logger.trace(pickler, "# Lo")
    return

