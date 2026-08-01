
def vecdot(x: Tensor, y: Tensor, dim: int = -1) -> Tensor:
    check_fp_or_complex(x.dtype, "linalg.vecdot")
    return (x.conj() * y).sum(dim=dim)


def vecdot(x1: Array, x2: Array, /, xp: Namespace, *, axis: int = -1) -> Array:
    if x1.shape[axis] != x2.shape[axis]:
        raise ValueError("x1 and x2 must have the same size along the given axis")

    if hasattr(xp, "broadcast_tensors"):
        _broadcast = xp.broadcast_tensors
    else:
        _broadcast = xp.broadcast_arrays

    x1_ = xp.moveaxis(x1, axis, -1)
    x2_ = xp.moveaxis(x2, axis, -1)
    x1_, x2_ = _broadcast(x1_, x2_)

    res = xp.conj(x1_[..., None, :]) @ x2_[..., None]
    return res[..., 0, 0]


def vecdot(x1: Array, x2: Array, /, *, axis: int = -1, **kwargs: object) -> Array:
    from ._aliases import isdtype

    x1, x2 = _fix_promotion(x1, x2, only_scalar=False)

    # torch.linalg.vecdot incorrectly allows broadcasting along the contracted dimension
    if x1.shape[axis] != x2.shape[axis]:
        raise ValueError("x1 and x2 must have the same size along the given axis")

    # torch.linalg.vecdot doesn't support integer dtypes
    if isdtype(x1.dtype, 'integral') or isdtype(x2.dtype, 'integral'):
        if kwargs:
            raise RuntimeError("vecdot kwargs not supported for integral dtypes")

        x1_ = torch.moveaxis(x1, axis, -1)
        x2_ = torch.moveaxis(x2, axis, -1)
        x1_, x2_ = torch.broadcast_tensors(x1_, x2_)

        res = x1_[..., None, :] @ x2_[..., None]
        return res[..., 0, 0]
    return torch.linalg.vecdot(x1, x2, dim=axis, **kwargs)


def vecdot(x1: Array, x2: Array, /, *, axis: int = -1) -> Array:
    x1, x2 = _fix_promotion(x1, x2, only_scalar=False)
    return _vecdot(x1, x2, axis=axis)


def vecdot(x1, x2, /, *, axis=-1):
    """
    Computes the vector dot product.

    This function is restricted to arguments compatible with the Array API,
    contrary to :func:`numpy.vecdot`.

    Let :math:`\\mathbf{a}` be a vector in ``x1`` and :math:`\\mathbf{b}` be
    a corresponding vector in ``x2``. The dot product is defined as:

    .. math::
       \\mathbf{a} \\cdot \\mathbf{b} = \\sum_{i=0}^{n-1} \\overline{a_i}b_i

    over the dimension specified by ``axis`` and where :math:`\\overline{a_i}`
    denotes the complex conjugate if :math:`a_i` is complex and the identity
    otherwise.

    Parameters
    ----------
    x1 : array_like
        First input array.
    x2 : array_like
        Second input array.
    axis : int, optional
        Axis over which to compute the dot product. Default: ``-1``.

    Returns
    -------
    output : ndarray
        The vector dot product of the input.

    See Also
    --------
    numpy.vecdot

    Examples
    --------
    Get the projected size along a given normal for an array of vectors.

    >>> v = np.array([[0., 5., 0.], [0., 0., 10.], [0., 6., 8.]])
    >>> n = np.array([0., 0.6, 0.8])
    >>> np.linalg.vecdot(v, n)
    array([ 3.,  8., 10.])

    """
    return _core_vecdot(x1, x2, axis=axis)


def vecdot(x1: ArrayLike, x2: ArrayLike, /, *, axis: int = -1,
           precision: lax.PrecisionLike = None,
           preferred_element_type: DTypeLike | None = None) -> Array:
  """Compute the (batched) vector conjugate dot product of two arrays.

  JAX implementation of :func:`numpy.linalg.vecdot`.

  Args:
    x1: left-hand side array.
    x2: right-hand side array. Size of ``x2[axis]`` must match size of ``x1[axis]``,
      and remaining dimensions must be broadcast-compatible.
    axis: axis along which to compute the dot product (default: -1)
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``x1`` and ``x2``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array containing the conjugate dot product of ``x1`` and ``x2`` along ``axis``.
    The non-contracted dimensions are broadcast together.

  See also:
    - :func:`jax.numpy.vecdot`: similar API in the ``jax.numpy`` namespace.
    - :func:`jax.numpy.linalg.matmul`: matrix multiplication.
    - :func:`jax.numpy.linalg.tensordot`: general tensor dot product.

  Examples:
    Vector dot product of two 1D arrays:

    >>> x1 = jnp.array([1, 2, 3])
    >>> x2 = jnp.array([4, 5, 6])
    >>> jnp.linalg.vecdot(x1, x2)
    Array(32, dtype=int32)

    Batched vector dot product of two 2D arrays:

    >>> x1 = jnp.array([[1, 2, 3],
    ...                 [4, 5, 6]])
    >>> x2 = jnp.array([[2, 3, 4]])
    >>> jnp.linalg.vecdot(x1, x2, axis=-1)
    Array([20, 47], dtype=int32)
  """
  x1, x2 = ensure_arraylike('jnp.linalg.vecdot', x1, x2)
  return tensor_contractions.vecdot(x1, x2, axis=axis, precision=precision,
                                    preferred_element_type=preferred_element_type)


def vecdot(x1: ArrayLike, x2: ArrayLike, /, *, axis: int = -1,
           precision: lax.PrecisionLike = None,
           preferred_element_type: DTypeLike | None = None) -> Array:
  """Perform a conjugate multiplication of two batched vectors.

  JAX implementation of :func:`numpy.vecdot`.

  Args:
    a: left-hand side array.
    b: right-hand side array. Size of ``b[axis]`` must match size of ``a[axis]``,
      and remaining dimensions must be broadcast-compatible.
    axis: axis along which to compute the dot product (default: -1)
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``a`` and ``b``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    array containing the conjugate dot product of ``a`` and ``b`` along ``axis``.
    The non-contracted dimensions are broadcast together.

  See Also:
    - :func:`jax.numpy.vdot`: flattened vector product.
    - :func:`jax.numpy.vecmat`: vector-matrix product.
    - :func:`jax.numpy.matmul`: general matrix multiplication.
    - :func:`jax.lax.dot_general`: general N-dimensional batched dot product.

  Examples:
    Vector conjugate-dot product of two 1D arrays:

    >>> a = jnp.array([1j, 2j, 3j])
    >>> b = jnp.array([4., 5., 6.])
    >>> jnp.linalg.vecdot(a, b)
    Array(0.-32.j, dtype=complex64)

    Batched vector dot product of two 2D arrays:

    >>> a = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> b = jnp.array([[2, 3, 4]])
    >>> jnp.linalg.vecdot(a, b, axis=-1)
    Array([20, 47], dtype=int32)
  """
  from jax._src.numpy.lax_numpy import moveaxis

  x1_arr, x2_arr = util.ensure_arraylike("jnp.vecdot", x1, x2)
  if x1_arr.shape[axis] != x2_arr.shape[axis]:
    raise ValueError(f"axes must match; got shapes {x1_arr.shape} and {x2_arr.shape} with {axis=}")
  x1_arr = moveaxis(x1_arr, axis, -1)
  x2_arr = moveaxis(x2_arr, axis, -1)
  return vectorize(partial(vdot, precision=precision, preferred_element_type=preferred_element_type),
                   signature="(n),(n)->()")(x1_arr, x2_arr)

