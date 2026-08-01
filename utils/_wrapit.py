
def _wrapit(obj, method, *args, **kwds):
    conv = _array_converter(obj)
    # As this already tried the method, subok is maybe quite reasonable here
    # but this follows what was done before. TODO: revisit this.
    arr, = conv.as_arrays(subok=False)
    result = getattr(arr, method)(*args, **kwds)

    return conv.wrap(result, to_scalar=False)

