
def _cases_axes_tuple_length_mismatch():
    # Generate combinations of filter function, valid kwargs, and
    # keyword-value pairs for which the value will become with mismatched
    # (invalid) size
    filter_func = ndimage.gaussian_filter
    kwargs = dict(radius=3, mode='constant', sigma=1.0, order=0)
    for key, val in kwargs.items():
        yield make_xp_pytest_param(filter_func, kwargs, key, val)

    filter_funcs = [ndimage.uniform_filter, ndimage.minimum_filter,
                    ndimage.maximum_filter]
    kwargs = dict(size=3, mode='constant', origin=0)
    for filter_func in filter_funcs:
        for key, val in kwargs.items():
            yield make_xp_pytest_param(filter_func, kwargs, key, val)

    filter_funcs = [ndimage.correlate, ndimage.convolve]
    # sequence of mode not supported for correlate or convolve
    kwargs = dict(origin=0)
    for filter_func in filter_funcs:
        for key, val in kwargs.items():
            yield make_xp_pytest_param(filter_func, kwargs, key, val)

