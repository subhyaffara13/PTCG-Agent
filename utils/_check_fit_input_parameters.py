
def _check_fit_input_parameters(dist, data, args, kwds):
    if not isinstance(data, CensoredData):
        data = np.asarray(data)

    floc = kwds.get('floc', None)
    fscale = kwds.get('fscale', None)

    num_shapes = len(dist.shapes.split(",")) if dist.shapes else 0
    fshape_keys = []
    fshapes = []

    # user has many options for fixing the shape, so here we standardize it
    # into 'f' + the number of the shape.
    # Adapted from `_reduce_func` in `_distn_infrastructure.py`:
    if dist.shapes:
        shapes = dist.shapes.replace(',', ' ').split()
        for j, s in enumerate(shapes):
            key = 'f' + str(j)
            names = [key, 'f' + s, 'fix_' + s]
            val = _get_fixed_fit_value(kwds, names)
            fshape_keys.append(key)
            fshapes.append(val)
            if val is not None:
                kwds[key] = val

    # determine if there are any unknown arguments in kwds
    known_keys = {'loc', 'scale', 'optimizer', 'method',
                  'floc', 'fscale', *fshape_keys}
    unknown_keys = set(kwds).difference(known_keys)
    if unknown_keys:
        raise TypeError(f"Unknown keyword arguments: {unknown_keys}.")

    if len(args) > num_shapes:
        raise TypeError("Too many positional arguments.")

    if None not in {floc, fscale, *fshapes}:
        # This check is for consistency with `rv_continuous.fit`.
        # Without this check, this function would just return the
        # parameters that were given.
        raise RuntimeError("All parameters fixed. There is nothing to "
                           "optimize.")

    uncensored = data._uncensor() if isinstance(data, CensoredData) else data
    if not np.isfinite(uncensored).all():
        raise ValueError("The data contains non-finite values.")

    return (data, *fshapes, floc, fscale)

