
def classify_arg(dist, arg, arg_domain):
    if arg is None:
        valid_args = np.ones(dist._shape, dtype=bool)
        endpoint_args = np.zeros(dist._shape, dtype=bool)
        outside_args = np.zeros(dist._shape, dtype=bool)
        nan_args = np.zeros(dist._shape, dtype=bool)
        return valid_args, endpoint_args, outside_args, nan_args

    a, b = arg_domain.get_numerical_endpoints(
        parameter_values=dist._parameters)

    a, b, arg = np.broadcast_arrays(a, b, arg)
    a_included, b_included = arg_domain.inclusive

    inside = (a <= arg) if a_included else a < arg
    inside &= (arg <= b) if b_included else arg < b
    # TODO: add `supported` method and check here
    on = np.zeros(a.shape, dtype=int)
    on[a == arg] = -1
    on[b == arg] = 1
    outside = np.zeros(a.shape, dtype=int)
    outside[(arg < a) if a_included else arg <= a] = -1
    outside[(b < arg) if b_included else b <= arg] = 1
    nan = np.isnan(arg)

    return inside, on, outside, nan

