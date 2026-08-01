
def _vectorize(xp):
    # xp-compatible version of np.vectorize
    # assumes arguments are all arrays of the same shape
    def decorator(f):
        def wrapped(*arg_arrays):
            shape = arg_arrays[0].shape
            arg_arrays = [xp_ravel(arg_array, xp=xp) for arg_array in arg_arrays]
            res = []
            for i in range(math.prod(shape)):
                arg_scalars = [arg_array[i] for arg_array in arg_arrays]
                res.append(f(*arg_scalars))
            return res

        return wrapped

    return decorator


def _vectorize(xp):
    # xp-compatible version of np.vectorize
    # assumes arguments are all arrays of the same shape
    def decorator(f):
        def wrapped(*arg_arrays):
            shape = arg_arrays[0].shape
            arg_arrays = [xp_ravel(arg_array) for arg_array in arg_arrays]
            res = []
            for i in range(math.prod(shape)):
                arg_scalars = [arg_array[i] for arg_array in arg_arrays]
                res.append(f(*arg_scalars))
            return res

        return wrapped

    return decorator

