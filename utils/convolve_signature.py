
def convolve_signature(input, weights, output=None, *args, **kwds):
    return array_namespace(input, weights, _skip_if_dtype(output))


def convolve_signature(in1, in2, *args, **kwds):
    return array_namespace(in1, in2)

