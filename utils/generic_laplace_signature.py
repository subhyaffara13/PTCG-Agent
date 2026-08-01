
def generic_laplace_signature(input, derivative2, output=None, *args, **kwds):
    # XXX: function LowLevelCallable w/backends
    return array_namespace(input, _skip_if_dtype(output))

