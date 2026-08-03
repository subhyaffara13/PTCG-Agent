import math


def clip(value: float, min_val: float = float("-inf"), max_val: float = float("inf")) -> float:
    return max(min_val, min(max_val, value))


def clip(
    a: ArrayLike,
    min: ArrayLike | None = None,
    max: ArrayLike | None = None,
    out: OutArray | None = None,
):
    return torch.clamp(a, min, max)


def clip(
    x: Array,
    /,
    min: float | Array | None = None,
    max: float | Array | None = None,
    *,
    xp: Namespace,
    # TODO: np.clip has other ufunc kwargs
    out: Array | None = None,
) -> Array:
    def _isscalar(a: object) -> TypeIs[float | None]:
        return isinstance(a, int | float) or a is None

    min_shape = () if _isscalar(min) else min.shape
    max_shape = () if _isscalar(max) else max.shape

    wrapped_xp = array_namespace(x)

    result_shape = xp.broadcast_shapes(x.shape, min_shape, max_shape)

    # np.clip does type promotion but the array API clip requires that the
    # output have the same dtype as x. We do this instead of just downcasting
    # the result of xp.clip() to handle some corner cases better (e.g.,
    # avoiding uint64 -> float64 promotion).

    # Note: cases where min or max overflow (integer) or round (float) in the
    # wrong direction when downcasting to x.dtype are unspecified. This code
    # just does whatever NumPy does when it downcasts in the assignment, but
    # other behavior could be preferred, especially for integers. For example,
    # this code produces:

    # >>> clip(asarray(0, dtype=int8), asarray(128, dtype=int16), None)
    # -128

    # but an answer of 0 might be preferred. See
    # https://github.com/numpy/numpy/issues/24976 for more discussion on this issue.

    # At least handle the case of Python integers correctly (see
    # https://github.com/numpy/numpy/pull/26892).
    if wrapped_xp.isdtype(x.dtype, "integral"):
        if type(min) is int and min <= wrapped_xp.iinfo(x.dtype).min:
            min = None
        if type(max) is int and max >= wrapped_xp.iinfo(x.dtype).max:
            max = None

    dev = _get_device(x)
    if out is None:
        out = wrapped_xp.empty(result_shape, dtype=x.dtype, device=dev)
    assert out is not None  # workaround for a type-narrowing issue in pyright
    out[()] = x

    if min is not None:
        a = wrapped_xp.asarray(min, dtype=x.dtype, device=dev)
        a = xp.broadcast_to(a, result_shape)
        ia = (out < a) | xp.isnan(a)
        out[ia] = a[ia]

    if max is not None:
        b = wrapped_xp.asarray(max, dtype=x.dtype, device=dev)
        b = xp.broadcast_to(b, result_shape)
        ib = (out > b) | xp.isnan(b)
        out[ib] = b[ib]

    # Return a scalar for 0-D
    return out[()]


def clip(
    x: Array,
    /,
    min: int | float | Array | None = None,
    max: int | float | Array | None = None,
    **kwargs
) -> Array:
    def _isscalar(a: object):
        return isinstance(a, int | float) or a is None

    # cf clip in common/_aliases.py
    if not x.is_floating_point():
        if type(min) is int and min <= torch.iinfo(x.dtype).min:
            min = None
        if type(max) is int and max >= torch.iinfo(x.dtype).max:
            max = None

    if min is None and max is None:
        return torch.clone(x)

    min_is_scalar = _isscalar(min)
    max_is_scalar = _isscalar(max)

    if min_is_scalar and max_is_scalar:
        if (min is not None and math.isnan(min)) or (max is not None and math.isnan(max)):
            # edge case: torch.clamp(torch.zeros(1), float('nan')) -> tensor(0.)
            # https://github.com/pytorch/pytorch/issues/172067
            return torch.full_like(x, fill_value=torch.nan)
        return torch.clamp(x, min, max, **kwargs)

    # pytorch has (tensor, tensor, tensor) and (tensor, scalar, scalar) signatures,
    # but does not accept (tensor, scalar, tensor)
    a_min = min
    if min is not None and min_is_scalar:
        a_min = torch.as_tensor(min, dtype=x.dtype, device=x.device)

    a_max = max
    if max is not None and max_is_scalar:
        a_max = torch.as_tensor(max, dtype=x.dtype, device=x.device)

    return torch.clamp(x, a_min, a_max, **kwargs)


def clip(
    x: Array,
    /,
    min: float | Array | None = None,
    max: float | Array | None = None,
) -> Array:
    """
    Array API compatibility wrapper for clip().

    See the corresponding documentation in the array library and/or the array API
    specification for more details.
    """

    def _isscalar(a: float | Array | None, /) -> TypeIs[float | None]:
        return a is None or isinstance(a, (int, float))

    min_shape = () if _isscalar(min) else min.shape
    max_shape = () if _isscalar(max) else max.shape

    # TODO: This won't handle dask unknown shapes
    result_shape = np.broadcast_shapes(x.shape, min_shape, max_shape)

    if min is not None:
        min = da.broadcast_to(da.asarray(min), result_shape)
    if max is not None:
        max = da.broadcast_to(da.asarray(max), result_shape)

    if min is None and max is None:
        return da.positive(x)

    if min is None:
        return astype(da.minimum(x, max), x.dtype)
    if max is None:
        return astype(da.maximum(x, min), x.dtype)

    return astype(da.minimum(da.maximum(x, min), max), x.dtype)


def clip(max_delta: jax.typing.ArrayLike) -> base.GradientTransformation:
  """Clips updates element-wise, to be in ``[-max_delta, +max_delta]``.

  Args:
    max_delta: The maximum absolute value for each element in the update.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def update_fn(updates, state, params=None):
    del params
    return optax.tree.clip(updates, -max_delta, max_delta), state

  return base.GradientTransformation(base.init_empty_state, update_fn)


def clip(a, a_min=np._NoValue, a_max=np._NoValue, out=None, *,
         min=np._NoValue, max=np._NoValue, **kwargs):
    """
    Clip (limit) the values in an array.

    Given an interval, values outside the interval are clipped to
    the interval edges.  For example, if an interval of ``[0, 1]``
    is specified, values smaller than 0 become 0, and values larger
    than 1 become 1.

    Equivalent to but faster than ``np.minimum(a_max, np.maximum(a, a_min))``.

    No check is performed to ensure ``a_min < a_max``.

    Parameters
    ----------
    a : array_like
        Array containing elements to clip.
    a_min, a_max : array_like or None
        Minimum and maximum value. If ``None``, clipping is not performed on
        the corresponding edge. If both ``a_min`` and ``a_max`` are ``None``,
        the elements of the returned array stay the same. Both are broadcasted
        against ``a``.
    out : ndarray, optional
        The results will be placed in this array. It may be the input
        array for in-place clipping.  `out` must be of the right shape
        to hold the output.  Its type is preserved.
    min, max : array_like or None
        Array API compatible alternatives for ``a_min`` and ``a_max``
        arguments. Either ``a_min`` and ``a_max`` or ``min`` and ``max``
        can be passed at the same time. Default: ``None``.

        .. versionadded:: 2.1.0
    **kwargs
        For other keyword-only arguments, see the
        :ref:`ufunc docs <ufuncs.kwargs>`.

    Returns
    -------
    clipped_array : ndarray
        An array with the elements of `a`, but where values
        < `a_min` are replaced with `a_min`, and those > `a_max`
        with `a_max`.

    See Also
    --------
    :ref:`ufuncs-output-type`

    Notes
    -----
    When `a_min` is greater than `a_max`, `clip` returns an
    array in which all values are equal to `a_max`,
    as shown in the second example.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(10)
    >>> a
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> np.clip(a, 1, 8)
    array([1, 1, 2, 3, 4, 5, 6, 7, 8, 8])
    >>> np.clip(a, 8, 1)
    array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    >>> np.clip(a, 3, 6, out=a)
    array([3, 3, 3, 3, 4, 5, 6, 6, 6, 6])
    >>> a
    array([3, 3, 3, 3, 4, 5, 6, 6, 6, 6])
    >>> a = np.arange(10)
    >>> a
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> np.clip(a, [3, 4, 1, 1, 1, 4, 4, 4, 4, 4], 8)
    array([3, 4, 2, 3, 4, 5, 6, 7, 8, 8])

    """
    if a_min is np._NoValue and a_max is np._NoValue:
        a_min = None if min is np._NoValue else min
        a_max = None if max is np._NoValue else max
    elif a_min is np._NoValue:
        raise TypeError("clip() missing 1 required positional "
                        "argument: 'a_min'")
    elif a_max is np._NoValue:
        raise TypeError("clip() missing 1 required positional "
                        "argument: 'a_max'")
    elif min is not np._NoValue or max is not np._NoValue:
        raise ValueError("Passing `min` or `max` keyword argument when "
                         "`a_min` and `a_max` are provided is forbidden.")

    return _wrapfunc(a, 'clip', a_min, a_max, out=out, **kwargs)


def clip(
  arr: ArrayLike | None = None,
  /,
  min: ArrayLike | None = None,
  max: ArrayLike | None = None,
) -> Array:
  """Clip array values to a specified range.

  JAX implementation of :func:`numpy.clip`.

  Args:
    arr: N-dimensional array to be clipped.
    min: optional minimum value of the clipped range; if ``None`` (default) then
      result will not be clipped to any minimum value. If specified, it should be
      broadcast-compatible with ``arr`` and ``max``.
    max: optional maximum value of the clipped range; if ``None`` (default) then
      result will not be clipped to any maximum value. If specified, it should be
      broadcast-compatible with ``arr`` and ``min``.

  Returns:
    An array containing values from ``arr``, with values smaller than ``min`` set
    to ``min``, and values larger than ``max`` set to ``max``.
    Wherever ``min`` is larger than ``max``, the value of ``max`` is returned.

  See also:
    - :func:`jax.numpy.minimum`: Compute the element-wise minimum value of two arrays.
    - :func:`jax.numpy.maximum`: Compute the element-wise maximum value of two arrays.

  Examples:
    >>> arr = jnp.array([0, 1, 2, 3, 4, 5, 6, 7])
    >>> jnp.clip(arr, 2, 5)
    Array([2, 2, 2, 3, 4, 5, 5, 5], dtype=int32)
  """
  if arr is None:
    raise ValueError("No input was provided to the clip function.")

  util.check_arraylike("clip", arr)
  if any(iscomplexobj(t) for t in (arr, min, max)):
    raise ValueError(
      "Clip received a complex value either through the input or the min/max "
      "keywords. Complex values have no ordering and cannot be clipped. "
      "Please convert to a real value or array by taking the real or "
      "imaginary components via jax.numpy.real/imag respectively.")
  if min is not None:
    arr = ufuncs.maximum(min, arr)
  if max is not None:
    arr = ufuncs.minimum(max, arr)
  return asarray(arr)

