
def save_socket(pickler, obj):
    logger.trace(pickler, "So: %s", obj)
    pickler.save_reduce(*reduce_socket(obj))
    logger.trace(pickler, "# So")
    return

