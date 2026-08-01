
def validateaxis(axis, *, ndim=2) -> tuple[int, ...] | None:
    if axis is None:
        return None

    if axis == ():
        raise ValueError(
            "sparse does not accept 0D axis (). Either use toarray (for dense) "
            "or copy (for sparse)."
        )

    if not isinstance(axis, tuple):
        # If not a tuple, check that the provided axis is actually
        # an integer and raise a TypeError similar to NumPy's
        if not np.issubdtype(np.dtype(type(axis)), np.integer):
            raise TypeError(f'axis must be an integer/tuple of ints, not {type(axis)}')
        axis = (axis,)

    canon_axis = []
    for ax in axis:
        if not isintlike(ax):
            raise TypeError(f"axis must be an integer. (given {ax})")
        if ax < 0:
            ax += ndim
        if ax < 0 or ax >= ndim:
            raise ValueError("axis out of range for ndim")
        canon_axis.append(ax)

    len_axis = len(canon_axis)
    if len_axis != len(set(canon_axis)):
        raise ValueError("duplicate value in axis")
    elif len_axis > ndim:
        raise ValueError("axis tuple has too many elements")
    elif len_axis == ndim:
        return None
    else:
        return tuple(canon_axis)

