
def _stack_dispatcher(arrays, axis=None, out=None, *,
                      dtype=None, casting=None):
    arrays = _arrays_for_stack_dispatcher(arrays)
    if out is not None:
        # optimize for the typical case where only arrays is provided
        arrays = list(arrays)
        arrays.append(out)
    return arrays

