
def spline_filter1d_signature(
    input, order=3, axis=-1, output=np.float64, *args, **kwds
):
    return array_namespace(input, _skip_if_dtype(output))

