
def save_weakproxy(pickler, obj):
    # Must do string substitution here and use %r to avoid ReferenceError.
    logger.trace(pickler, "R2: %r" % obj)
    refobj = _locate_object(_proxy_helper(obj))
    pickler.save_reduce(_create_weakproxy, (refobj, callable(obj)), obj=obj)
    logger.trace(pickler, "# R2")
    return

