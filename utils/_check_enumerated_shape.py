
def _check_enumerated_shape(shape):
    for s in shape:
        if not isinstance(s, (list, tuple)):
            return False
    return True

