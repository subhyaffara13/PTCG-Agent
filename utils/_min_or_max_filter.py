
def _min_or_max_filter(input, size, footprint, structure, output, mode,
                       cval, origin, minimum, axes=None):
    if (size is not None) and (footprint is not None):
        warnings.warn("ignoring size because footprint is set",
                      UserWarning, stacklevel=3)
    if structure is None:
        if footprint is None:
            if size is None:
                raise RuntimeError("no footprint provided")
            separable = True
        else:
            footprint = np.asarray(footprint, dtype=bool)
            if not footprint.any():
                raise ValueError("All-zero footprint is not supported.")
            if footprint.all():
                size = footprint.shape
                footprint = None
                separable = True
            else:
                separable = False
    else:
        structure = np.asarray(structure, dtype=np.float64)
        separable = False
        if footprint is None:
            footprint = np.ones(structure.shape, bool)
        else:
            footprint = np.asarray(footprint, dtype=bool)
    input = np.asarray(input)
    if np.iscomplexobj(input):
        raise TypeError("Complex type not supported")
    output = _ni_support._get_output(output, input)
    temp_needed = np.may_share_memory(input, output)
    if temp_needed:
        # input and output arrays cannot share memory
        temp = output
        output = _ni_support._get_output(output.dtype, input)
    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    if separable:
        origins = _ni_support._normalize_sequence(origin, num_axes)
        sizes = _ni_support._normalize_sequence(size, num_axes)
        modes = _ni_support._normalize_sequence(mode, num_axes)
        axes = [(axes[ii], sizes[ii], origins[ii], modes[ii])
                for ii in range(len(axes)) if sizes[ii] > 1]
        if minimum:
            filter_ = minimum_filter1d
        else:
            filter_ = maximum_filter1d
        if len(axes) > 0:
            for axis, size, origin, mode in axes:
                filter_(input, int(size), axis, output, mode, cval, origin)
                input = output
        else:
            output[...] = input[...]
    else:
        # expand origins and footprint if num_axes < input.ndim
        footprint = _expand_footprint(input.ndim, axes, footprint)
        origins = _expand_origin(input.ndim, axes, origin)

        fshape = [ii for ii in footprint.shape if ii > 0]
        if len(fshape) != input.ndim:
            raise RuntimeError(f"footprint.ndim ({footprint.ndim}) must match "
                               f"len(axes) ({len(axes)})")
        for origin, lenf in zip(origins, fshape):
            if (lenf // 2 + origin < 0) or (lenf // 2 + origin >= lenf):
                raise ValueError("invalid origin")
        if not footprint.flags.contiguous:
            footprint = footprint.copy()
        if structure is not None:
            if len(structure.shape) != num_axes:
                raise RuntimeError("structure array has incorrect shape")
            if num_axes != structure.ndim:
                structure = np.expand_dims(
                    structure,
                    tuple(ax for ax in range(structure.ndim) if ax not in axes)
                )
            if not structure.flags.contiguous:
                structure = structure.copy()
        if not isinstance(mode, str) and isinstance(mode, Iterable):
            raise RuntimeError(
                "A sequence of modes is not supported for non-separable "
                "footprints")
        mode = _ni_support._extend_mode_to_code(mode)
        _nd_image.min_or_max_filter(input, footprint, structure, output,
                                    mode, cval, origins, minimum)
    if temp_needed:
        temp[...] = output
        output = temp
    return output

