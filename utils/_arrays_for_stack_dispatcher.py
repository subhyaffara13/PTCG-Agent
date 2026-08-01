
def _arrays_for_stack_dispatcher(arrays):
    if not hasattr(arrays, "__getitem__"):
        raise TypeError('arrays to stack must be passed as a "sequence" type '
                        'such as list or tuple.')

    return tuple(arrays)

