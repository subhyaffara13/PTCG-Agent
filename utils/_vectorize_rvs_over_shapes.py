
def _vectorize_rvs_over_shapes(_rvs1):
    """Decorator that vectorizes _rvs method to work on ndarray shapes"""
    # _rvs1 must be a _function_ that accepts _scalar_ args as positional
    # arguments, `size` and `random_state` as keyword arguments.
    # _rvs1 must return a random variate array with shape `size`. If `size` is
    # None, _rvs1 must return a scalar.
    # When applied to _rvs1, this decorator broadcasts ndarray args
    # and loops over them, calling _rvs1 for each set of scalar args.
    # For usage example, see _nchypergeom_gen
    def _rvs(*args, size, random_state):
        _rvs1_size, _rvs1_indices = _check_shape(args[0].shape, size)

        size = np.array(size)
        _rvs1_size = np.array(_rvs1_size)
        _rvs1_indices = np.array(_rvs1_indices)

        if np.all(_rvs1_indices):  # all args are scalars
            return _rvs1(*args, size, random_state)

        out = np.empty(size)

        # out.shape can mix dimensions associated with arg_shape and _rvs1_size
        # Sort them to arg_shape + _rvs1_size for easy indexing of dimensions
        # corresponding with the different sets of scalar args
        j0 = np.arange(out.ndim)
        j1 = np.hstack((j0[~_rvs1_indices], j0[_rvs1_indices]))
        out = np.moveaxis(out, j1, j0)

        for i in np.ndindex(*size[~_rvs1_indices]):
            # arg can be squeezed because singleton dimensions will be
            # associated with _rvs1_size, not arg_shape per _check_shape
            out[i] = _rvs1(*[np.squeeze(arg)[i] for arg in args],
                           _rvs1_size, random_state)

        return np.moveaxis(out, j0, j1)  # move axes back before returning
    return _rvs

