
def spline_filter_signature(input, order=3, output=np.float64, *args, **kwds):
    return array_namespace(input, _skip_if_dtype(output))


def spline_filter_signature(Iin, lmbda=5.0):
    return array_namespace(Iin)

