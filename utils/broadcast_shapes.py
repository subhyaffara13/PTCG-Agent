import math


def broadcast_shapes(*shapes):
    r"""broadcast_shapes(*shapes) -> Size

    Similar to :func:`broadcast_tensors` but for shapes.

    This is equivalent to
    ``torch.broadcast_tensors(*map(torch.empty, shapes))[0].shape``
    but avoids the need create to intermediate tensors. This is useful for
    broadcasting tensors of common batch shape but different rightmost shape,
    e.g. to broadcast mean vectors with covariance matrices.

    Example::

        >>> torch.broadcast_shapes((2,), (3, 1), (1, 1, 1))
        torch.Size([1, 3, 2])

    Args:
        \*shapes (torch.Size): Shapes of tensors.

    Returns:
        shape (torch.Size): A shape compatible with all input shapes.

    Raises:
        RuntimeError: If shapes are incompatible.
    """
    # This wrapper exists to support variadic args.
    # TODO Move this to C++ once the jit has better support for torch.Size.
    if not torch.jit.is_tracing():
        result = torch._refs._broadcast_shapes(*shapes)
        if result is None:
            return torch.Size([])
        return torch.Size(result)
    else:
        # with implementation above, torch.jit.trace hardcodes the sizes which makes subsequent replays fail
        with torch.no_grad():
            scalar = torch.zeros((), device="cpu")
            tensors = [scalar.expand(shape) for shape in shapes]
            tensors = broadcast_tensors(*tensors)
            return tensors[0].shape


def broadcast_shapes(*args):
    return torch.broadcast_shapes(*args)


def broadcast_shapes(*shapes) -> ShapeType:
    return torch.Size(_broadcast_shapes(*shapes))


def broadcast_shapes(shape1, shape2):
    if len(shape1) <= 0:
        raise AssertionError(f"shape1 must have length > 0, got {len(shape1)}")
    if len(shape2) <= 0:
        raise AssertionError(f"shape2 must have length > 0, got {len(shape2)}")
    s1 = list(shape1)
    s2 = list(shape2)
    # TODO: Support non-equal-rank broadcast where semantics match.
    # This can be tricky for NHWC tensors because dimension orders
    # don't match between PT and NNAPI, even though semantics match.
    if len(s1) > len(s2):
        # s2 = [1] * (len(s1) - len(s2)) + s2
        raise Exception(  # noqa: TRY002
            "Non-equal-rank broadcast is not supported yet."
        )  # noqa: TRY002
    if len(s2) > len(s1):
        # s3 = [1] * (len(s2) - len(s1)) + s1
        raise Exception(  # noqa: TRY002
            "Non-equal-rank broadcast is not supported yet."
        )  # noqa: TRY002
    ret = []
    for d1, d2 in zip(s1, s2):
        if d1 == 1:
            ret.append(d2)
        elif d2 == 1:
            ret.append(d1)
        elif d1 == d2:
            ret.append(d1)
        else:
            raise Exception(  # noqa: TRY002
                f"Cannot broadcast shapes: {shape1} and {shape2}"
            )  # noqa: TRY002
    return tuple(ret)


def broadcast_shapes(*shapes):
    """Check if shapes can be broadcast and return resulting shape

    This is similar to the NumPy ``broadcast_shapes`` function but
    does not check memory consequences of the resulting dense matrix.

    Parameters
    ----------
    *shapes : tuple of shape tuples
        The tuple of shapes to be considered for broadcasting.
        Shapes should be tuples of non-negative integers.

    Returns
    -------
    new_shape : tuple of integers
        The shape that results from broadcasting th input shapes.
    """
    if not shapes:
        return ()
    shapes = [shp if isinstance(shp, tuple | list) else (shp,) for shp in shapes]
    big_shp = max(shapes, key=len)
    out = list(big_shp)
    for shp in shapes:
        if shp is big_shp:
            continue
        for i, x in enumerate(shp, start=-len(shp)):
            if x != 1 and x != out[i]:
                if out[i] != 1:
                    raise ValueError("shapes cannot be broadcast to a single shape.")
                out[i] = x
    return (*out,)


def broadcast_shapes(*shapes: tuple[float | None, ...]) -> tuple[int | None, ...]:
    """
    Compute the shape of the broadcasted arrays.

    Duplicates :func:`numpy.broadcast_shapes`, with additional support for
    None and NaN sizes.

    This is equivalent to ``xp.broadcast_arrays(arr1, arr2, ...)[0].shape``
    without needing to worry about the backend potentially deep copying
    the arrays.

    Parameters
    ----------
    *shapes : tuple[int | None, ...]
        Shapes of the arrays to broadcast.

    Returns
    -------
    tuple[int | None, ...]
        The shape of the broadcasted arrays.

    See Also
    --------
    numpy.broadcast_shapes : Equivalent NumPy function.
    array_api.broadcast_arrays : Function to broadcast actual arrays.

    Notes
    -----
    This function accepts the Array API's ``None`` for unknown sizes,
    as well as Dask's non-standard ``math.nan``.
    Regardless of input, the output always contains ``None`` for unknown sizes.

    Examples
    --------
    >>> import array_api_extra as xpx
    >>> xpx.broadcast_shapes((2, 3), (2, 1))
    (2, 3)
    >>> xpx.broadcast_shapes((4, 2, 3), (2, 1), (1, 3))
    (4, 2, 3)
    """
    if not shapes:
        return ()  # Match NumPy output

    ndim = max(len(shape) for shape in shapes)
    out: list[int | None] = []
    for axis in range(-ndim, 0):
        sizes = {shape[axis] for shape in shapes if axis >= -len(shape)}
        # Dask uses NaN for unknown shape, which predates the Array API spec for None
        none_size = None in sizes or math.nan in sizes  # noqa: PLW0177
        sizes -= {1, None, math.nan}
        if len(sizes) > 1:
            msg = (
                "shape mismatch: objects cannot be broadcast to a single shape: "
                f"{shapes}."
            )
            raise ValueError(msg)
        out.append(None if none_size else cast(int, sizes.pop()) if sizes else 1)

    return tuple(out)


def broadcast_shapes(*args):
    """
    Broadcast the input shapes into a single shape.

    :ref:`Learn more about broadcasting here <basics.broadcasting>`.

    .. versionadded:: 1.20.0

    Parameters
    ----------
    *args : tuples of ints, or ints
        The shapes to be broadcast against each other.

    Returns
    -------
    tuple
        Broadcasted shape.

    Raises
    ------
    ValueError
        If the shapes are not compatible and cannot be broadcast according
        to NumPy's broadcasting rules.

    See Also
    --------
    broadcast
    broadcast_arrays
    broadcast_to

    Examples
    --------
    >>> import numpy as np
    >>> np.broadcast_shapes((1, 2), (3, 1), (3, 2))
    (3, 2)

    >>> np.broadcast_shapes((6, 7), (5, 6, 1), (7,), (5, 1, 7))
    (5, 6, 7)
    """
    arrays = [np.empty(x, dtype=_size0_dtype) for x in args]
    return _broadcast_shape(*arrays)


def broadcast_shapes(*shapes: tuple[int, ...]) -> tuple[int, ...]:
  ...


def broadcast_shapes(*shapes: tuple[int | core.Tracer, ...]
                     ) -> tuple[int | core.Tracer, ...]:
  ...


def broadcast_shapes(*shapes):
  """Returns the shape that results from NumPy broadcasting of `shapes`.

  This follows the rules of `NumPy broadcasting`_.

  Args:
    shapes: one or more tuples of integers containing the shapes of arrays
      to be broadcast.

  Returns:
    A tuple of integers representing the broadcasted shape.

  Raises:
    ValueError: if shapes are not broadcast-compatible.

  See Also:
    - :func:`jax.numpy.broadcast_shapes`: similar API in the JAX NumPy namespace

  Examples:
    Some examples of broadcasting compatible shapes:

    >>> jnp.broadcast_shapes((1,), (4,))
    (4,)
    >>> jnp.broadcast_shapes((3, 1), (4,))
    (3, 4)
    >>> jnp.broadcast_shapes((3, 1), (1, 4), (5, 1, 1))
    (5, 3, 4)

    Error when attempting to broadcast incompatible shapes:

    >>> jnp.broadcast_shapes((3, 1), (4, 1))  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Incompatible shapes for broadcasting: shapes=[(3, 1), (4, 1)]

  .. _NumPy broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
  """
  # NOTE: We have both cached and uncached versions to handle Tracers in shapes.
  try:
    return _broadcast_shapes_cached(*shapes)
  except:
    return _broadcast_shapes_uncached(*shapes)


def broadcast_shapes(*shapes: Sequence[int]) -> tuple[int, ...]:
  ...


def broadcast_shapes(*shapes: Sequence[int | core.Tracer]
                     ) -> tuple[int | core.Tracer, ...]:
  ...


def broadcast_shapes(*shapes):
  """Broadcast input shapes to a common output shape.

  JAX implementation of :func:`numpy.broadcast_shapes`. JAX uses NumPy-style
  broadcasting rules, which you can read more about at `NumPy broadcasting`_.

  Args:
    shapes: 0 or more shapes specified as sequences of integers

  Returns:
    The broadcasted shape as a tuple of integers.

  See Also:
    - :func:`jax.numpy.broadcast_arrays`: broadcast arrays to a common shape.
    - :func:`jax.numpy.broadcast_to`: broadcast an array to a specified shape.

  Examples:
    Some compatible shapes:

    >>> jnp.broadcast_shapes((1,), (4,))
    (4,)
    >>> jnp.broadcast_shapes((3, 1), (4,))
    (3, 4)
    >>> jnp.broadcast_shapes((3, 1), (1, 4), (5, 1, 1))
    (5, 3, 4)

    Incompatible shapes:

    >>> jnp.broadcast_shapes((3, 1), (4, 1))  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: Incompatible shapes for broadcasting: shapes=[(3, 1), (4, 1)]

  .. _NumPy broadcasting: https://numpy.org/doc/stable/user/basics.broadcasting.html
  """
  if not shapes:
    return ()
  shapes = [(shape,) if np.ndim(shape) == 0 else tuple(shape) for shape in shapes]
  return lax.broadcast_shapes(*shapes)

