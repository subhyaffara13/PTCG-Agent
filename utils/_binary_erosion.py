
def _binary_erosion(input, structure, iterations, mask, output,
                    border_value, origin, invert, brute_force, axes):
    try:
        iterations = operator.index(iterations)
    except TypeError as e:
        raise TypeError('iterations parameter should be an integer') from e

    input = np.asarray(input)
    # The Cython code can't cope with broadcasted inputs
    if not input.flags.c_contiguous and not input.flags.f_contiguous:
        input = np.ascontiguousarray(input)

    ndim = input.ndim
    if np.iscomplexobj(input):
        raise TypeError('Complex type not supported')
    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    if structure is None:
        structure = generate_binary_structure(num_axes, 1)
    else:
        structure = np.asarray(structure, dtype=bool)
    if ndim > num_axes:
        structure = _filters._expand_footprint(ndim, axes, structure,
                                               footprint_name="structure")

    if structure.ndim != input.ndim:
        raise RuntimeError('structure and input must have same dimensionality')
    if not structure.flags.contiguous:
        structure = structure.copy()
    if structure.size < 1:
        raise RuntimeError('structure must not be empty')
    if mask is not None:
        mask = np.asarray(mask)
        if mask.shape != input.shape:
            raise RuntimeError('mask and input must have equal sizes')
    origin = _ni_support._normalize_sequence(origin, num_axes)
    origin = _filters._expand_origin(ndim, axes, origin)
    cit = _center_is_true(structure, origin)
    if isinstance(output, np.ndarray):
        if np.iscomplexobj(output):
            raise TypeError('Complex output type not supported')
    else:
        output = bool
    output = _ni_support._get_output(output, input)
    temp_needed = np.may_share_memory(input, output)
    if temp_needed:
        # input and output arrays cannot share memory
        temp = output
        output = _ni_support._get_output(output.dtype, input)
    if iterations == 1:
        _nd_image.binary_erosion(input, structure, mask, output,
                                 border_value, origin, invert, cit, 0)
    elif cit and not brute_force:
        changed, coordinate_list = _nd_image.binary_erosion(
            input, structure, mask, output,
            border_value, origin, invert, cit, 1)
        structure = structure[tuple([slice(None, None, -1)] *
                                    structure.ndim)]
        for ii in range(len(origin)):
            origin[ii] = -origin[ii]
            if not structure.shape[ii] & 1:
                origin[ii] -= 1
        if mask is not None:
            mask = np.asarray(mask, dtype=np.int8)
        if not structure.flags.contiguous:
            structure = structure.copy()
        _nd_image.binary_erosion2(output, structure, mask, iterations - 1,
                                  origin, invert, coordinate_list)
    else:
        tmp_in = np.empty_like(input, dtype=bool)
        tmp_out = output
        if iterations >= 1 and not iterations & 1:
            tmp_in, tmp_out = tmp_out, tmp_in
        changed = _nd_image.binary_erosion(
            input, structure, mask, tmp_out,
            border_value, origin, invert, cit, 0)
        ii = 1
        while ii < iterations or (iterations < 1 and changed):
            tmp_in, tmp_out = tmp_out, tmp_in
            changed = _nd_image.binary_erosion(
                tmp_in, structure, mask, tmp_out,
                border_value, origin, invert, cit, 0)
            ii += 1
    if temp_needed:
        temp[...] = output
        output = temp
    return output

