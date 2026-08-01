
def save_context(pickler, obj):
    logger.trace(pickler, "Cx: %s", obj)
    pickler.save_reduce(ContextType, tuple(obj.items()), obj=obj)
    logger.trace(pickler, "# Cx")

