
def _check_arrays_broadcastable(arrays, axis):
    # https://numpy.org/doc/stable/user/basics.broadcasting.html
    # "When operating on two arrays, NumPy compares their shapes element-wise.
    # It starts with the trailing (i.e. rightmost) dimensions and works its
    # way left.
    # Two dimensions are compatible when
    # 1. they are equal, or
    # 2. one of them is 1
    # ...
    # Arrays do not need to have the same number of dimensions."
    # (Clarification: if the arrays are compatible according to the criteria
    #  above and an array runs out of dimensions, it is still compatible.)
    # Below, we follow the rules above except ignoring `axis`

    n_dims = max([arr.ndim for arr in arrays])
    if axis is not None:
        # convert to negative axis
        axis = (-n_dims + axis) if axis >= 0 else axis

    for dim in range(1, n_dims+1):  # we'll index from -1 to -n_dims, inclusive
        if -dim == axis:
            continue  # ignore lengths along `axis`

        dim_lengths = set()
        for arr in arrays:
            if dim <= arr.ndim and arr.shape[-dim] != 1:
                dim_lengths.add(arr.shape[-dim])

        if len(dim_lengths) > 1:
            return False
    return True

