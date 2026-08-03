import itertools

def check_shape(
    buffer: IndentedBuffer, var: CSEVariableType, shape: BlockShapeType
) -> None:
    backend = get_current_backend()
    assert shape is not None
    if config.test_configs.runtime_triton_shape_assert and backend == "triton":
        shape_str = (
            ", ".join(str(d) for d in shape) if len(shape) != 1 else f"{shape[0]},"
        )
        buffer.writeline(f"tl.static_assert({var}.shape == ({shape_str}))")


def check_shape(args, current_shape=None, *, allow_nd=(2,)) -> tuple[int, ...]:
    """Imitate numpy.matrix handling of shape arguments

    Parameters
    ----------
    args : array_like
        Data structures providing information about the shape of the sparse array.
    current_shape : tuple, optional
        The current shape of the sparse array or matrix.
        If None (default), the current shape will be inferred from args.
    allow_nd : tuple of ints, optional default: (2,)
        If shape does not have a length in the tuple allow_nd an error is raised.

    Returns
    -------
    new_shape: tuple
        The new shape after validation.
    """
    if len(args) == 0:
        raise TypeError("function missing 1 required positional argument: 'shape'")
    if len(args) == 1:
        try:
            shape_iter = iter(args[0])
        except TypeError:
            new_shape = (operator.index(args[0]), )
        else:
            new_shape = tuple(operator.index(arg) for arg in shape_iter)
    else:
        new_shape = tuple(operator.index(arg) for arg in args)

    if current_shape is None:
        if len(new_shape) not in allow_nd:
            raise ValueError(f'shape must have length in {allow_nd}. Got {new_shape=}')
        if any(d < 0 for d in new_shape):
            raise ValueError("'shape' elements cannot be negative")
    else:
        # Check the current size only if needed
        current_size = prod(current_shape)

        # Check for negatives
        negative_indexes = [i for i, x in enumerate(new_shape) if x < 0]
        if not negative_indexes:
            new_size = prod(new_shape)
            if new_size != current_size:
                raise ValueError(f'cannot reshape array of size {current_size}'
                                 f' into shape {new_shape}')
        elif len(negative_indexes) == 1:
            skip = negative_indexes[0]
            specified = prod(new_shape[:skip] + new_shape[skip+1:])
            unspecified, remainder = divmod(current_size, specified)
            if remainder != 0:
                err_shape = tuple('newshape' if x < 0 else x for x in new_shape)
                raise ValueError(f'cannot reshape array of size {current_size}'
                                 f' into shape {err_shape}')
            new_shape = new_shape[:skip] + (unspecified,) + new_shape[skip+1:]
        else:
            raise ValueError('can only specify one unknown dimension')

    if len(new_shape) not in allow_nd:
        raise ValueError(f'shape must have length in {allow_nd}. Got {new_shape=}')

    return new_shape


def check_shape(interpolator_cls, x_shape, y_shape, deriv_shape=None, axis=0,
                extra_args=None):
    if extra_args is None:
        extra_args = {}
    rng = np.random.RandomState(1234)

    x = [-1, 0, 1, 2, 3, 4]
    s = list(range(1, len(y_shape)+1))
    s.insert(axis % (len(y_shape)+1), 0)
    y = rng.rand(*((6,) + y_shape)).transpose(s)

    xi = np.zeros(x_shape)
    if interpolator_cls is CubicHermiteSpline:
        dydx = rng.rand(*((6,) + y_shape)).transpose(s)
        yi = interpolator_cls(x, y, dydx, axis=axis, **extra_args)(xi)
    else:
        yi = interpolator_cls(x, y, axis=axis, **extra_args)(xi)

    target_shape = ((deriv_shape or ()) + y.shape[:axis]
                    + x_shape + y.shape[axis:][1:])
    assert yi.shape == target_shape

    # check it works also with lists
    if x_shape and y.size > 0:
        if interpolator_cls is CubicHermiteSpline:
            interpolator_cls(list(x), list(y), list(dydx), axis=axis,
                             **extra_args)(list(xi))
        else:
            interpolator_cls(list(x), list(y), axis=axis,
                             **extra_args)(list(xi))

    # check also values
    if xi.size > 0 and deriv_shape is None:
        bs_shape = y.shape[:axis] + (1,)*len(x_shape) + y.shape[axis:][1:]
        yv = y[((slice(None,),)*(axis % y.ndim)) + (1,)]
        yv = yv.reshape(bs_shape)

        yi, y = np.broadcast_arrays(yi, yv)
        xp_assert_close(yi, y)


def check_shape(shape, /, **kwargs):
    """
    For each *key, value* pair in *kwargs*, check that *value* has the shape *shape*;
    if not, raise an appropriate ValueError.

    *None* in the shape is treated as a "free" size that can have any length.
    e.g. (None, 2) -> (N, 2)

    The values checked must be numpy arrays.

    Examples
    --------
    To check for (N, 2) shaped arrays

    >>> _api.check_shape((None, 2), arg=arg, other_arg=other_arg)
    """
    for k, v in kwargs.items():
        data_shape = v.shape

        if (len(data_shape) != len(shape)
                or any(s != t and t is not None for s, t in zip(data_shape, shape))):
            dim_labels = iter(itertools.chain(
                'NMLKJIH',
                (f"D{i}" for i in itertools.count())))
            text_shape = ", ".join([str(n) if n is not None else next(dim_labels)
                                    for n in shape[::-1]][::-1])
            if len(shape) == 1:
                text_shape += ","

            raise ValueError(
                f"{k!r} must be {len(shape)}D with shape ({text_shape}), "
                f"but your input has shape {v.shape}"
            )

