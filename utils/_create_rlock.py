
def _create_rlock(count, owner, *args): #XXX: ignores 'blocking'
    lock = RLockType()
    if owner is not None:
        lock._acquire_restore((count, owner))
    if owner and not lock._is_owned():
        raise UnpicklingError("Cannot acquire lock")
    return lock

