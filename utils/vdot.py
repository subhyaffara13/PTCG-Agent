
def vdot(a: ArrayLike, b: ArrayLike, /):
    # 1. torch only accepts 1D arrays, numpy flattens
    # 2. torch requires matching dtype, while numpy casts (?)
    t_a, t_b = torch.atleast_1d(a, b)
    if t_a.ndim > 1:
        t_a = t_a.flatten()
    if t_b.ndim > 1:
        t_b = t_b.flatten()

    dtype = _dtypes_impl.result_type_impl(t_a, t_b)
    is_half = dtype == torch.float16 and (t_a.is_cpu or t_b.is_cpu)
    is_bool = dtype == torch.bool

    # work around torch's "dot" not implemented for 'Half', 'Bool'
    if is_half:
        dtype = torch.float32
    elif is_bool:
        dtype = torch.uint8

    t_a = _util.cast_if_needed(t_a, dtype)
    t_b = _util.cast_if_needed(t_b, dtype)

    result = torch.vdot(t_a, t_b)

    if is_half:
        result = result.to(torch.float16)
    elif is_bool:
        result = result.to(torch.bool)

    return result


def vdot(self, other):
    if not self.is_complex():
        return torch.dot(self, other)

    if self.is_conj():
        if other.is_conj():
            return torch.vdot(other.conj(), self.conj())
        else:
            return torch.dot(self.conj(), other)
    elif other.is_conj():
        return torch.dot(self, other.conj()).conj()

    # The decomposition fails if you do self.conj()... not sure why
    return (self.conj_physical() * other).sum()


def vdot(a, b, /):
    r"""
    vdot(a, b, /)

    Return the dot product of two vectors.

    The `vdot` function handles complex numbers differently than `dot`:
    if the first argument is complex, it is replaced by its complex conjugate
    in the dot product calculation. `vdot` also handles multidimensional
    arrays differently than `dot`: it does not perform a matrix product, but
    flattens the arguments to 1-D arrays before taking a vector dot product.

    Consequently, when the arguments are 2-D arrays of the same shape, this
    function effectively returns their
    `Frobenius inner product <https://en.wikipedia.org/wiki/Frobenius_inner_product>`_
    (also known as the *trace inner product* or the *standard inner product*
    on a vector space of matrices).

    Parameters
    ----------
    a : array_like
        If `a` is complex the complex conjugate is taken before calculation
        of the dot product.
    b : array_like
        Second argument to the dot product.

    Returns
    -------
    output : ndarray
        Dot product of `a` and `b`.  Can be an int, float, or
        complex depending on the types of `a` and `b`.

    See Also
    --------
    dot : Return the dot product without using the complex conjugate of the
          first argument.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1+2j,3+4j])
    >>> b = np.array([5+6j,7+8j])
    >>> np.vdot(a, b)
    (70-8j)
    >>> np.vdot(b, a)
    (70+8j)

    Note that higher-dimensional arrays are flattened!

    >>> a = np.array([[1, 4], [5, 6]])
    >>> b = np.array([[4, 1], [2, 2]])
    >>> np.vdot(a, b)
    30
    >>> np.vdot(b, a)
    30
    >>> 1*4 + 4*1 + 5*2 + 6*2
    30

    """
    return (a, b)


def vdot(
    a: ArrayLike, b: ArrayLike, *,
    precision: lax.PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
) -> Array:
  """Perform a conjugate multiplication of two 1D vectors.

  JAX implementation of :func:`numpy.vdot`.

  Args:
    a: first input array, if not 1D it will be flattened.
    b: second input array, if not 1D it will be flattened. Must have ``a.size == b.size``.
    precision: either ``None`` (default), which means the default precision for
      the backend, a :class:`~jax.lax.Precision` enum value (``Precision.DEFAULT``,
      ``Precision.HIGH`` or ``Precision.HIGHEST``) or a tuple of two
      such values indicating precision of ``a`` and ``b``.
    preferred_element_type: either ``None`` (default), which means the default
      accumulation type for the input types, or a datatype, indicating to
      accumulate results to and return a result with that datatype.

  Returns:
    Scalar array (shape ``()``) containing the conjugate vector product of the inputs.

  See Also:
    - :func:`jax.numpy.vecdot`: batched vector product.
    - :func:`jax.numpy.matmul`: general matrix multiplication.
    - :func:`jax.lax.dot_general`: general N-dimensional batched dot product.

  Examples:
    >>> x = jnp.array([1j, 2j, 3j])
    >>> y = jnp.array([1., 2., 3.])
    >>> jnp.vdot(x, y)
    Array(0.-14.j, dtype=complex64)

    Note the difference between this and :func:`~jax.numpy.dot`, which does not
    conjugate the first input when complex:

    >>> jnp.dot(x, y)
    Array(0.+14.j, dtype=complex64)
  """
  a, b = util.ensure_arraylike("vdot", a, b)
  if dtypes.issubdtype(a.dtype, np.complexfloating):
    a = ufuncs.conj(a)
  return dot(a.ravel(), b.ravel(), precision=precision,
             preferred_element_type=preferred_element_type)

