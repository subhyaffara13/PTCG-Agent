
def minimum(validator, minimum, instance, schema):
    if not validator.is_type(instance, "number"):
        return

    if instance < minimum:
        message = f"{instance!r} is less than the minimum of {minimum!r}"
        yield ValidationError(message)


def minimum(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.minimum(a, b)


def minimum(a, b):
    mask = a < b
    if is_floating(a):
        mask |= a != a
    return tl.where(mask, a, b)


def minimum(g: jit_utils.GraphContext, input, other):
    # pyrefly: ignore [no-matching-overload]
    return min(g, input, dim_or_y=other)


def minimum(g: jit_utils.GraphContext, input, other):
    # pyrefly: ignore [no-matching-overload]
    return min(g, input, dim_or_y=other)


def minimum(f, symbol, domain=S.Reals):
    """
    Returns the minimum value of a function in the given domain.

    Parameters
    ==========

    f : :py:class:`~.Expr`
        The concerned function.
    symbol : :py:class:`~.Symbol`
        The variable for minimum value needs to be determined.
    domain : :py:class:`~.Interval`
        The domain over which the minimum have to be checked.
        If unspecified, then the global minimum is returned.

    Returns
    =======

    number
        Minimum value of the function in the given domain.

    Examples
    ========

    >>> from sympy import Interval, Symbol, S, sin, cos, minimum
    >>> x = Symbol('x')

    >>> f = x**2 + 2*x + 5
    >>> minimum(f, x, S.Reals)
    4

    >>> minimum(sin(x), x, Interval(2, 3))
    sin(3)

    >>> minimum(sin(x)*cos(x), x)
    -1/2

    """
    if isinstance(symbol, Symbol):
        if domain is S.EmptySet:
            raise ValueError("Minimum value not defined for empty domain.")

        return function_range(f, symbol, domain).inf
    else:
        raise ValueError("%s is not a valid symbol." % symbol)


def minimum(input, labels=None, index=None):
    """
    Calculate the minimum of the values of an array over labeled regions.

    Parameters
    ----------
    input : array_like
        Array_like of values. For each region specified by `labels`, the
        minimal values of `input` over the region is computed.
    labels : array_like, optional
        An array_like of integers marking different regions over which the
        minimum value of `input` is to be computed. `labels` must have the
        same shape as `input`. If `labels` is not specified, the minimum
        over the whole array is returned.
    index : array_like, optional
        A list of region labels that are taken into account for computing the
        minima. If index is None, the minimum over all elements where `labels`
        is non-zero is returned.

    Returns
    -------
    output : a scalar or list of integers or floats based on input type.
        List of minima of `input` over the regions determined by `labels` and
        whose index is in `index`. If `index` or `labels` are not specified, a
        float is returned: the minimal value of `input` if `labels` is None,
        and the minimal value of elements where `labels` is greater than zero
        if `index` is None.

    See Also
    --------
    label, maximum, median, minimum_position, extrema, sum, mean, variance,
    standard_deviation

    Notes
    -----
    The function returns a Python list and not a NumPy array, use
    `np.array` to convert the list to an array.

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.array([[1, 2, 0, 0],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])
    >>> labels, labels_nb = ndimage.label(a)
    >>> labels
    array([[1, 1, 0, 0],
           [1, 1, 0, 2],
           [0, 0, 0, 2],
           [3, 3, 0, 0]], dtype=int32)
    >>> ndimage.minimum(a, labels=labels, index=np.arange(1, labels_nb + 1))
    [1, 4, 3]
    >>> ndimage.minimum(a)
    0
    >>> ndimage.minimum(a, labels=labels)
    1

    """
    return _select(input, labels, index, find_min=True)[0]


def minimum(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MinOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def minimum(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MinOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def minimum(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Return element-wise minimum of the input arrays.

  JAX implementation of :obj:`numpy.minimum`.

  Args:
    x: input array or scalar.
    y: input array or scalar. Both ``x`` and ``y`` should either have same shape
      or be broadcast compatible.

  Returns:
    An array containing the element-wise minimum of ``x`` and ``y``.

  Note:
    For each pair of elements, ``jnp.minimum`` returns:
      - smaller of the two if both elements are finite numbers.
      - ``nan`` if one element is ``nan``.

  See also:
    - :func:`jax.numpy.maximum`: Returns element-wise maximum of the input arrays.
    - :func:`jax.numpy.fmin`: Returns element-wise minimum of the input arrays,
      ignoring NaNs.
    - :func:`jax.numpy.amin`: Returns the minimum of array elements along a given
      axis.
    - :func:`jax.numpy.nanmin`: Returns the minimum of the array elements along
      a given axis, ignoring NaNs.

  Examples:
    Inputs with ``x.shape == y.shape``:

    >>> x = jnp.array([2, 3, 5, 1])
    >>> y = jnp.array([-3, 6, -4, 7])
    >>> jnp.minimum(x, y)
    Array([-3,  3, -4,  1], dtype=int32)

    Inputs having broadcast compatibility:

    >>> x1 = jnp.array([[1, 5, 2],
    ...                 [-3, 4, 7]])
    >>> y1 = jnp.array([-2, 3, 6])
    >>> jnp.minimum(x1, y1)
    Array([[-2,  3,  2],
           [-3,  3,  6]], dtype=int32)

    Inputs with ``nan``:

    >>> nan = jnp.nan
    >>> x2 = jnp.array([[2.5, nan, -2],
    ...                 [nan, 5, 6],
    ...                 [-4, 3, 7]])
    >>> y2 = jnp.array([1, nan, 5])
    >>> jnp.minimum(x2, y2)
    Array([[ 1., nan, -2.],
           [nan, nan,  5.],
           [-4., nan,  5.]], dtype=float32)
  """
  return lax.min(*promote_args("minimum", x, y))

