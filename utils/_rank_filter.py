
def _rank_filter(input, rank, size=None, footprint=None, output=None,
                 mode="reflect", cval=0.0, origin=0, operation='rank',
                 axes=None):
    if (size is not None) and (footprint is not None):
        warnings.warn("ignoring size because footprint is set",
                      UserWarning, stacklevel=3)
    input = np.asarray(input)
    if np.iscomplexobj(input):
        raise TypeError('Complex type not supported')
    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    if footprint is None:
        if size is None:
            raise RuntimeError("no footprint or filter size provided")
        sizes = _ni_support._normalize_sequence(size, num_axes)
        footprint = np.ones(sizes, dtype=bool)
    else:
        footprint = np.asarray(footprint, dtype=bool)
    # expand origins, footprint and modes if num_axes < input.ndim
    footprint = _expand_footprint(input.ndim, axes, footprint)
    origins = _expand_origin(input.ndim, axes, origin)
    mode = _expand_mode(input.ndim, axes, mode)

    fshape = [ii for ii in footprint.shape if ii > 0]
    if len(fshape) != input.ndim:
        raise RuntimeError(f"footprint.ndim ({footprint.ndim}) must match "
                           f"len(axes) ({len(axes)})")
    for origin, lenf in zip(origins, fshape):
        if (lenf // 2 + origin < 0) or (lenf // 2 + origin >= lenf):
            raise ValueError('invalid origin')
    if not footprint.flags.contiguous:
        footprint = footprint.copy()
    filter_size = np.where(footprint, 1, 0).sum()
    if operation == 'median':
        rank = filter_size // 2
    elif operation == 'percentile':
        percentile = rank
        if percentile < 0.0:
            percentile += 100.0
        if percentile < 0 or percentile > 100:
            raise RuntimeError('invalid percentile')
        if percentile == 100.0:
            rank = filter_size - 1
        else:
            rank = int(float(filter_size) * percentile / 100.0)
    if rank < 0:
        rank += filter_size
    if rank < 0 or rank >= filter_size:
        raise RuntimeError('rank not within filter footprint size')
    if rank == 0:
        return minimum_filter(input, None, footprint, output, mode, cval,
                              origins, axes=None)
    elif rank == filter_size - 1:
        return maximum_filter(input, None, footprint, output, mode, cval,
                              origins, axes=None)
    else:
        output = _ni_support._get_output(output, input)
        temp_needed = np.may_share_memory(input, output)
        if temp_needed:
            # input and output arrays cannot share memory
            temp = output
            output = _ni_support._get_output(output.dtype, input)
        if not isinstance(mode, str) and isinstance(mode, Iterable):
            raise RuntimeError(
                "A sequence of modes is not supported by non-separable rank "
                "filters")
        mode = _ni_support._extend_mode_to_code(mode, is_filter=True)
        # Some corner cases are currently not allowed to use the
        # "new"/fast 1D rank filter code, including when the
        # footprint is large compared to the array size.
        # See discussion in gh-23293; longer-term it may be possible
        # to allow the fast path for these corner cases as well,
        # if algorithmic fixes are found.
        lim2 = input.size - ((footprint.size - 1) // 2 - origin)
        if input.ndim == 1 and ((lim2 >= 0) or (input.size == 1)):
            if input.dtype in (np.int64, np.float64, np.float32):
                x = input
                x_out = output
            elif input.dtype == np.float16:
                x = input.astype('float32')
                x_out = np.empty(x.shape, dtype='float32')
            elif np.result_type(input, np.int64) == np.int64:
                x = input.astype('int64')
                x_out = np.empty(x.shape, dtype='int64')
            elif input.dtype.kind in 'biu':
                # cast any other boolean, integer or unsigned type to int64
                x = input.astype('int64')
                x_out = np.empty(x.shape, dtype='int64')
            else:
                raise RuntimeError('Unsupported array type')
            cval = x.dtype.type(cval)
            _rank_filter_1d.rank_filter(x, rank, footprint.size, x_out, mode, cval,
                                        origin)
            if input.dtype not in (np.int64, np.float64, np.float32):
                np.copyto(output, x_out, casting='unsafe')
        else:
            _nd_image.rank_filter(input, rank, footprint, output, mode, cval, origins)
        if temp_needed:
            temp[...] = output
            output = temp
        return output

