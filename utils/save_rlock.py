
def save_rlock(pickler, obj):
    logger.trace(pickler, "RL: %s", obj)
    r = obj.__repr__() # don't use _release_save as it unlocks the lock
    count = int(r.split('count=')[1].split()[0].rstrip('>'))
    owner = int(r.split('owner=')[1].split()[0])
    pickler.save_reduce(_create_rlock, (count,owner,), obj=obj)
    logger.trace(pickler, "# RL")
    return

