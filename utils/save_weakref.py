
def save_weakref(pickler, obj):
    refobj = obj()
    logger.trace(pickler, "R1: %s", obj)
   #refobj = ctypes.pythonapi.PyWeakref_GetObject(obj) # dead returns "None"
    pickler.save_reduce(_create_weakref, (refobj,), obj=obj)
    logger.trace(pickler, "# R1")
    return

