
def maximum(validator, maximum, instance, schema):
    if not validator.is_type(instance, "number"):
        return

    if instance > maximum:
        message = f"{instance!r} is greater than the maximum of {maximum!r}"
        yield ValidationError(message)


def maximum(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.maximum(a, b)


def maximum(a, b):
    mask = a > b
    if is_floating(a):
        mask |= a != a
    return tl.where(mask, a, b)


def maximum(g: jit_utils.GraphContext, input, other):
    # pyrefly: ignore [no-matching-overload]
    return max(g, input, dim_or_y=other)


def maximum(g: jit_utils.GraphContext, input, other):
    # pyrefly: ignore [no-matching-overload]
    return max(g, input, dim_or_y=other)


def maximum(f, symbol, domain=S.Reals):
    """
    Returns the maximum value of a function in the given domain.

    Parameters
    ==========

    f : :py:class:`~.Expr`
        The concerned function.
    symbol : :py:class:`~.Symbol`
        The variable for maximum value needs to be determined.
    domain : :py:class:`~.Interval`
        The domain over which the maximum have to be checked.
        If unspecified, then the global maximum is returned.

    Returns
    =======

    number
        Maximum value of the function in given domain.

    Examples
    ========

    >>> from sympy import Interval, Symbol, S, sin, cos, pi, maximum
    >>> x = Symbol('x')

    >>> f = -x**2 + 2*x + 5
    >>> maximum(f, x, S.Reals)
    6

    >>> maximum(sin(x), x, Interval(-pi, pi/4))
    sqrt(2)/2

    >>> maximum(sin(x)*cos(x), x)
    1/2

    """
    if isinstance(symbol, Symbol):
        if domain is S.EmptySet:
            raise ValueError("Maximum value not defined for empty domain.")

        return function_range(f, symbol, domain).sup
    else:
        raise ValueError("%s is not a valid symbol." % symbol)


def maximum(input, labels=None, index=None):
    """
    Calculate the maximum of the values of an array over labeled regions.

    Parameters
    ----------
    input : array_like
        Array_like of values. For each region specified by `labels`, the
        maximal values of `input` over the region is computed.
    labels : array_like, optional
        An array of integers marking different regions over which the
        maximum value of `input` is to be computed. `labels` must have the
        same shape as `input`. If `labels` is not specified, the maximum
        over the whole array is returned.
    index : array_like, optional
        A list of region labels that are taken into account for computing the
        maxima. If index is None, the maximum over all elements where `labels`
        is non-zero is returned.

    Returns
    -------
    output : a scalar or list of integers or floats based on input type.
        List of maxima of `input` over the regions determined by `labels` and
        whose index is in `index`. If `index` or `labels` are not specified, a
        float is returned: the maximal value of `input` if `labels` is None,
        and the maximal value of elements where `labels` is greater than zero
        if `index` is None.

    See Also
    --------
    label, minimum, median, maximum_position, extrema, sum, mean, variance,
    standard_deviation

    Notes
    -----
    The function returns a Python list and not a NumPy array, use
    `np.array` to convert the list to an array.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(16).reshape((4,4))
    >>> a
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])
    >>> labels = np.zeros_like(a)
    >>> labels[:2,:2] = 1
    >>> labels[2:, 1:3] = 2
    >>> labels
    array([[1, 1, 0, 0],
           [1, 1, 0, 0],
           [0, 2, 2, 0],
           [0, 2, 2, 0]])
    >>> from scipy import ndimage
    >>> ndimage.maximum(a)
    15
    >>> ndimage.maximum(a, labels=labels, index=[1,2])
    [5, 14]
    >>> ndimage.maximum(a, labels=labels)
    14

    >>> b = np.array([[1, 2, 0, 0],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])
    >>> labels, labels_nb = ndimage.label(b)
    >>> labels
    array([[1, 1, 0, 0],
           [1, 1, 0, 2],
           [0, 0, 0, 2],
           [3, 3, 0, 0]], dtype=int32)
    >>> ndimage.maximum(b, labels=labels, index=np.arange(1, labels_nb + 1))
    [5, 7, 9]

    """
    return _select(input, labels, index, find_max=True)[0]


def maximum(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MaxOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def maximum(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MaxOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def maximum(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Return element-wise maximum of the input arrays.

  JAX implementation of :obj:`numpy.maximum`.

  Args:
    x: input array or scalar.
    y: input array or scalar. Both ``x`` and ``y`` should either have same shape
      or be broadcast compatible.

  Returns:
    An array containing the element-wise maximum of ``x`` and ``y``.

  Note:
    For each pair of elements, ``jnp.maximum`` returns:
      - larger of the two if both elements are finite numbers.
      - ``nan`` if one element is ``nan``.

  See also:
    - :func:`jax.numpy.minimum`: Returns element-wise minimum of the input
      arrays.
    - :func:`jax.numpy.fmax`: Returns element-wise maximum of the input arrays,
      ignoring NaNs.
    - :func:`jax.numpy.amax`: Returns the maximum of array elements along a given
      axis.
    - :func:`jax.numpy.nanmax`: Returns the maximum of the array elements along
      a given axis, ignoring NaNs.

  Examples:
    Inputs with ``x.shape == y.shape``:

    >>> x = jnp.array([1, -5, 3, 2])
    >>> y = jnp.array([-2, 4, 7, -6])
    >>> jnp.maximum(x, y)
    Array([1, 4, 7, 2], dtype=int32)

    Inputs with broadcast compatibility:

    >>> x1 = jnp.array([[-2, 5, 7, 4],
    ...                 [1, -6, 3, 8]])
    >>> y1 = jnp.array([-5, 3, 6, 9])
    >>> jnp.maximum(x1, y1)
    Array([[-2,  5,  7,  9],
           [ 1,  3,  6,  9]], dtype=int32)

    Inputs having ``nan``:

    >>> nan = jnp.nan
    >>> x2 = jnp.array([nan, -3, 9])
    >>> y2 = jnp.array([[4, -2, nan],
    ...                 [-3, -5, 10]])
    >>> jnp.maximum(x2, y2)
    Array([[nan, -2., nan],
          [nan, -3., 10.]], dtype=float32)
  """
  return lax.max(*promote_args("maximum", x, y))

