
def _vectorized_filter_iv(input, function, size, footprint, output, mode, cval, origin,
                          axes, batch_memory):
    xp = array_namespace(input, footprint, output)

    # vectorized_filter input validation and standardization
    input = xp.asarray(input)

    if not callable(function):
        raise ValueError("`function` must be a callable.")

    if size is None and footprint is None:
        raise ValueError("Either `size` or `footprint` must be provided.")

    if size is not None and footprint is not None:
        raise ValueError("Either `size` or `footprint` may be provided, not both.")

    if axes is None:
        axes = tuple(range(-input.ndim, 0))
    elif np.isscalar(axes):
        axes = (axes,)
    n_axes = len(axes)
    n_batch = input.ndim - n_axes

    if n_axes > input.ndim:
        message = ("The length of `axes` may not exceed the dimensionality of `input`"
                   "(`input.ndim`).")
        raise ValueError(message)

    # Either footprint or size must be provided
    footprinted_function = function
    if size is not None:
        # If provided, size must be an integer or tuple of integers.
        size = (size,)*n_axes if np.isscalar(size) else tuple(size)
        valid = [xp.isdtype(xp.asarray(i).dtype, 'integral') and i > 0 for i in size]
        if not all(valid):
            raise ValueError("All elements of `size` must be positive integers.")
    else:
        # If provided, `footprint` must be array-like
        footprint = xp.asarray(footprint, dtype=xp.bool)
        size = footprint.shape
        def footprinted_function(input, *args, axis=-1, **kwargs):
            return function(input[..., footprint], *args, axis=-1, **kwargs)

    # And by now, the dimensionality of the footprint must equal the number of axes
    if n_axes != len(size):
        message = ("`axes` must be compatible with the dimensionality "
                   "of the window specified by `size` or `footprint`.")
        raise ValueError(message)

    # If this is not *equal* to the dimensionality of `input`, then `axes`
    # must be a provided tuple, and its length must equal the core dimensionality.
    elif n_axes < input.ndim:
        if axes is None:
            message = ("`axes` must be provided if the dimensionality of the window "
                       "(`len(size)` or `footprint.ndim`) does not equal the number "
                       "of axes of `input` (`input.ndim`).")
            raise ValueError(message)
    else:
        axes = tuple(range(-n_axes, 0)) if axes is None else axes

    axes = (axes,) if np.isscalar(axes) else axes

    # If `origin` is provided, then it must be "broadcastable" to a tuple with length
    # equal to the core dimensionality.
    if origin is None:
        origin = (0,) * n_axes
    else:
        origin = (origin,)*n_axes if np.isscalar(origin) else tuple(origin)
        integral = [xp.isdtype(xp.asarray(i).dtype, 'integral') for i in origin]
        if not all(integral):
            raise ValueError("All elements of `origin` must be integers.")
        if not len(origin) == n_axes:
            message = ("`origin` must be an integer or tuple of integers with length "
                       "equal to the number of axes.")
            raise ValueError(message)

    # mode must be one of the allowed strings, and we should convert it to the
    # value required by `np.pad`/`cp.pad` here.
    valid_modes = {'reflect', 'constant', 'nearest', 'mirror', 'wrap',
                   'grid-mirror', 'grid-constant', 'grid-wrap', 'valid'}
    if mode not in valid_modes:
        raise ValueError(f"`mode` must be one of {valid_modes}.")
    mode_map = {'nearest': 'edge', 'reflect': 'symmetric', 'mirror': 'reflect',
                'grid-mirror': 'reflect', 'grid-constant': 'constant',
                'grid-wrap': 'wrap'}
    mode = mode_map.get(mode, mode)

    if mode == 'valid' and any(origin):
        raise ValueError("`mode='valid'` is incompatible with use of `origin`.")

    if cval is None:
        cval = 0.0
    elif mode != 'constant':
        raise ValueError("Use of `cval` is compatible only with `mode='constant'`.")

    # `cval` must be a scalar or "broadcastable" to a tuple with the same
    # dimensionality of `input`. (Full input validation done by `np.pad`/`cp.pad`.)
    if not xp.isdtype(xp.asarray(cval).dtype, 'numeric'):
        raise ValueError("`cval` must include only numbers.")

    # `batch_memory` must be a positive number.
    temp = xp.asarray(batch_memory)
    if temp.ndim != 0 or (not xp.isdtype(temp.dtype, 'numeric')) or temp <= 0:
        raise ValueError("`batch_memory` must be positive number.")

    # For simplicity, work with `axes` at the end.
    working_axes = tuple(range(-n_axes, 0))
    input = xp.moveaxis(input, axes, working_axes)
    output = (xp.moveaxis(output, axes, working_axes)
              if output is not None else output)

    # Wrap the function to limit maximum memory usage, deal with `footprint`,
    # and populate `output`. The latter requires some verbosity because we
    # don't know the output dtype.
    def wrapped_function(view, output=output):
        kwargs = {'axis': working_axes}

        if working_axes == ():
            return footprinted_function(xp.asarray(view), **kwargs)

        # for now, assume we only have to iterate over zeroth axis
        chunk_size = math.prod(view.shape[1:]) * view.dtype.itemsize
        slices_per_batch = min(view.shape[0], batch_memory // chunk_size)
        if slices_per_batch < 1:
            raise ValueError("`batch_memory` is insufficient for minimum chunk size.")

        elif slices_per_batch == view.shape[0]:
            if output is None:
                return footprinted_function(xp.asarray(view), **kwargs)
            else:
                output[...] = footprinted_function(xp.asarray(view), **kwargs)
                return output

        for i in range(0, view.shape[0], slices_per_batch):
            i2 = min(i + slices_per_batch, view.shape[0])
            if output is None:
                # Look at the dtype before allocating the array. (In a follow-up, we
                # can also look at the shape to support non-scalar elements.)
                temp = footprinted_function(xp.asarray(view[i:i2]), **kwargs)
                output = xp.empty(view.shape[:-n_axes], dtype=temp.dtype)
                output[i:i2, ...] = temp
            else:
                output[i:i2, ...] = footprinted_function(xp.asarray(view[i:i2]),
                                                         **kwargs)
        return output

    return (input, wrapped_function, size, mode, cval, origin,
            working_axes, axes, n_axes, n_batch, xp)

