
def _rref_typeof_on_owner(rref, blocking: bool = True):
    rref_type = type(rref.local_value())
    if blocking:
        return rref_type
    else:
        # Wrap result into a completed Future. This is so that if blocking=`False`
        # is specified, we return a future regardless of if this call is on user
        # or owner.
        future = Future[type]()
        future.set_result(rref_type)
        return future

