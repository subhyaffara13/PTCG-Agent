
def _correlate_or_convolve(input, weights, output, mode, cval, origin,
                           convolution, axes):
    input = np.asarray(input)
    weights = np.asarray(weights)
    complex_input = input.dtype.kind == 'c'
    complex_weights = weights.dtype.kind == 'c'
    if complex_input or complex_weights:
        if complex_weights and not convolution:
            # As for np.correlate, conjugate weights rather than input.
            weights = weights.conj()
        kwargs = dict(
            mode=mode, origin=origin, convolution=convolution, axes=axes
        )
        output = _ni_support._get_output(output, input, complex_output=True)

        return _complex_via_real_components(_correlate_or_convolve, input,
                                            weights, output, cval, **kwargs)

    axes = _ni_support._check_axes(axes, input.ndim)
    weights = np.asarray(weights, dtype=np.float64)

    # expand weights and origins if num_axes < input.ndim
    weights = _expand_footprint(input.ndim, axes, weights, "weights")
    origins = _expand_origin(input.ndim, axes, origin)

    wshape = [ii for ii in weights.shape if ii > 0]
    if len(wshape) != input.ndim:
        raise RuntimeError(f"weights.ndim ({len(wshape)}) must match "
                           f"len(axes) ({len(axes)})")
    if convolution:
        weights = weights[tuple([slice(None, None, -1)] * weights.ndim)]
        for ii in range(len(origins)):
            origins[ii] = -origins[ii]
            if not weights.shape[ii] & 1:
                origins[ii] -= 1
    for origin, lenw in zip(origins, wshape):
        if _invalid_origin(origin, lenw):
            raise ValueError('Invalid origin; origin must satisfy '
                             '-(weights.shape[k] // 2) <= origin[k] <= '
                             '(weights.shape[k]-1) // 2')

    if not weights.flags.contiguous:
        weights = weights.copy()
    output = _ni_support._get_output(output, input)
    temp_needed = np.may_share_memory(input, output)
    if temp_needed:
        # input and output arrays cannot share memory
        temp = output
        output = _ni_support._get_output(output.dtype, input)
    if not isinstance(mode, str) and isinstance(mode, Iterable):
        raise RuntimeError("A sequence of modes is not supported")
    mode = _ni_support._extend_mode_to_code(mode)
    _nd_image.correlate(input, weights, output, mode, cval, origins)
    if temp_needed:
        temp[...] = output
        output = temp
    return output

