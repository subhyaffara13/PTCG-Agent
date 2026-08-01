
def _unpickle_as_weakref(referent: object) -> weakref.ref[object]:
    return weakref.ref(referent)

