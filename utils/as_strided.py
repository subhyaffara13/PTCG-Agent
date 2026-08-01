
def as_strided(x, size, stride, storage_offset=None):
    new_device = None
    new_dtype = None
    if isinstance(x, TensorBox) and isinstance(x.data, ir.BaseView):
        # Note: Merging views
        # When we use as_strided, we can rewrite the size/stride/offset
        # of the incoming buffer x. If x is a view, we would overwrite
        # its metadata. Except for dtype, which we need to propagate.

        # Technically device is not needed because it is not possible
        # to have a cross-device view today.
        new_device = x.get_device()
        new_dtype = x.dtype
        x = x.data.unwrap_view()
    x.realize()
    if not ir.is_storage_and_layout(x):
        raise NotImplementedError(f"unrealized as_strided({x}, ...)")
    storage, old_layout = ir.as_storage_and_layout(x)
    new_layout = ir.FixedLayout(
        new_device if new_device else old_layout.device,
        new_dtype if new_dtype else old_layout.dtype,
        [sympy.expand(s) for s in size],
        [sympy.expand(s) for s in stride],
        sympy.expand(storage_offset or 0),
    )
    return TensorBox(ir.ReinterpretView(data=storage, layout=new_layout))


def as_strided(
    a: TensorLikeType,
    size: ShapeType,
    stride: StrideType,
    storage_offset: int | None = None,
) -> TensorLikeType:
    storage_offset_int = (
        storage_offset if storage_offset is not None else a.storage_offset()
    )
    return prims.as_strided(a, size, stride, storage_offset_int)


def as_strided(g: jit_utils.GraphContext, self, sizes, strides, offset=None):
    sizes = symbolic_helper._maybe_get_const(sizes, "is")
    rank = len(strides)
    self_1d = symbolic_helper._reshape_helper(
        g, self, g.op("Constant", value_t=torch.tensor([-1], dtype=torch.int64))
    )
    ind: torch.Tensor | None
    if not symbolic_helper._is_value(sizes):
        ind = torch.tensor([0], dtype=torch.long)
        for i, (size, stride) in enumerate(zip(sizes, strides)):
            r_size = [1] * rank
            r_size[i] = -1
            ind = ind + torch.arange(size).view(r_size) * stride
        if offset:
            ind = ind + offset
        return g.op("Gather", self_1d, g.op("Constant", value_t=ind))
    else:
        ind = None
        for i, stride in enumerate(strides):
            r_size = [1] * rank
            r_size[i] = -1
            size = select(
                g,
                sizes,
                g.op("Constant", value_t=torch.tensor([0])),
                g.op("Constant", value_t=torch.tensor(i)),
            )
            tmp_ind = symbolic_helper._reshape_helper(
                g,
                arange(g, size, 4, None, None, None),
                g.op("Constant", value_t=torch.tensor(r_size)),
            )
            tmp_ind = g.op(
                "Mul", tmp_ind, g.op("Constant", value_t=torch.tensor([stride]))
            )
            if ind is None:
                ind = tmp_ind
            else:
                ind = g.op("Add", ind, tmp_ind)
        if offset:
            # pyrefly: ignore [bad-argument-type]
            ind = g.op("Add", ind, g.op("Constant", torch.tensor([offset])))
        # pyrefly: ignore [bad-argument-type]
        return g.op("Gather", self_1d, ind)


def as_strided(
    x, shape=None, strides=None, subok=False, writeable=True, *, check_bounds=None
):
    """
    Create a view into the array with the given shape and strides.

    .. warning:: This function has to be used with extreme care, see notes.

    Parameters
    ----------
    x : ndarray
        Array to create a new.
    shape : sequence of int, optional
        The shape of the new array. Defaults to ``x.shape``.
    strides : sequence of int, optional
        The strides of the new array. Defaults to ``x.strides``.
    subok : bool, optional
        If True, subclasses are preserved.
    writeable : bool, optional
        If set to False, the returned array will always be readonly.
        Otherwise it will be writable if the original array was. It
        is advisable to set this to False if possible (see Notes).
    check_bounds : bool or None
        Check new stride and shape for potential out of bound memory
        access.

    Returns
    -------
    view : ndarray

    Raises
    ------
    ValueError
        If `check_bounds` is True the given shape and strides could result in
        out-of-bounds memory access.

    See also
    --------
    broadcast_to : broadcast an array to a given shape.
    reshape : reshape an array.
    lib.stride_tricks.sliding_window_view :
        userfriendly and safe function for a creation of sliding window views.

    Notes
    -----
    `as_strided` creates a view into the array given the exact strides
    and shape. This means it manipulates the internal data structure of
    ndarray and, if done incorrectly, the array elements can point to
    invalid memory and can corrupt results or crash your program.
    It is advisable to always use the original ``x.strides`` when
    calculating new strides to avoid reliance on a contiguous memory
    layout.

    Furthermore, arrays created with this function often contain self
    overlapping memory, so that two elements are identical.
    Vectorized write operations on such arrays will typically be
    unpredictable. They may even give different results for small, large,
    or transposed arrays.

    Since writing to these arrays has to be tested and done with great
    care, you may want to use ``writeable=False`` to avoid accidental write
    operations.

    For these reasons it is advisable to avoid `as_strided` when
    possible.

    Examples
    --------

    >>> import numpy as np
    ... from numpy.lib.stride_tricks import as_strided
    ... x = np.arange(10)
    ... y = as_strided(x, shape=(5,), strides=(8,), check_bounds=True)
    ... y
    array([0, 1, 2, 3, 4])

    Attempting to create an out-of-bounds view and use ``check_bounds=True``
    as_strided will raises an error:

    >>> as_strided(x, shape=(20,), strides=(8,), check_bounds=True)
    Traceback (most recent call last):
    ...
    ValueError: Given shape and strides would access memory out of bounds...

    When working with views, bounds are checked against the base array:

    >>> a = np.arange(1000)
    ... b = a[:2]
    ... c = as_strided(b, shape=(2,), strides=(400,), check_bounds=True)
    ... c[0], c[1]
    (0, 50)
    """

    # first convert input to array, possibly keeping subclass
    base = np.array(x, copy=None, subok=subok)
    interface = dict(base.__array_interface__)
    if shape is not None:
        interface['shape'] = tuple(shape)
    if strides is not None:
        interface['strides'] = tuple(strides)

    array = np.asarray(DummyArray(interface, base=base))
    # The route via `__interface__` does not preserve structured
    # dtypes. Since dtype should remain unchanged, we set it explicitly.
    array._set_dtype(base.dtype)

    view = _maybe_view_as_subclass(base, array)

    if view.flags.writeable and not writeable:
        view.flags.writeable = False

    if check_bounds:
        while isinstance(base.base, np.ndarray):
            base = base.base

        base_low, base_high = byte_bounds(base)
        view_low, view_high = byte_bounds(view)

        if view_low < base_low:
            raise ValueError(
                f"Given shape and strides would access memory out of bounds. "
                f"View starts {base_low - view_low} bytes before lowest address"
            )

        if view_high > base_high:
            raise ValueError(
                f"Given shape and strides would access memory out of bounds. "
                f"View ends {view_high - base_high} bytes after highest address"
            )

    return view

