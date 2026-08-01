
def capsule_new(p):
    return PyCapsule_New(addressof(p), None, None)

