
def generic_filter_signature(
    input, function, size=None, footprint=None, output=None, *args, **kwds
):
    # XXX: function LowLevelCallable w/backends
    return array_namespace(input, footprint, _skip_if_dtype(output))

