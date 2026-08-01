
def generic_gradient_magnitude_signature(
    input, derivative, output=None, *args, **kwds
):
    # XXX: function LowLevelCallable w/backends
    return array_namespace(input, _skip_if_dtype(output))

