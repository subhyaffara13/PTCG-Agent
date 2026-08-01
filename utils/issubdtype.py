
def issubdtype(arg1, arg2):
    # cf https://github.com/numpy/numpy/blob/v1.24.0/numpy/core/numerictypes.py#L356-L420

    # We also accept strings even if NumPy doesn't as dtypes are serialized as their
    # string representation in dynamo's graph
    def str_to_abstract(t):
        if isinstance(t, str) and t in _abstract_dtypes:
            return globals()[t]
        return t

    arg1 = str_to_abstract(arg1)
    arg2 = str_to_abstract(arg2)

    if not issubclass_(arg1, generic):
        arg1 = dtype(arg1).type
    if not issubclass_(arg2, generic):
        arg2 = dtype(arg2).type
    return issubclass(arg1, arg2)


def issubdtype(arg1, arg2):
    r"""
    Returns True if first argument is a typecode lower/equal in type hierarchy.

    This is like the builtin :func:`issubclass`, but for `dtype`\ s.

    Parameters
    ----------
    arg1, arg2 : dtype_like
        `dtype` or object coercible to one

    Returns
    -------
    out : bool

    See Also
    --------
    :ref:`arrays.scalars` : Overview of the numpy type hierarchy.

    Examples
    --------
    `issubdtype` can be used to check the type of arrays:

    >>> ints = np.array([1, 2, 3], dtype=np.int32)
    >>> np.issubdtype(ints.dtype, np.integer)
    True
    >>> np.issubdtype(ints.dtype, np.floating)
    False

    >>> floats = np.array([1, 2, 3], dtype=np.float32)
    >>> np.issubdtype(floats.dtype, np.integer)
    False
    >>> np.issubdtype(floats.dtype, np.floating)
    True

    Similar types of different sizes are not subdtypes of each other:

    >>> np.issubdtype(np.float64, np.float32)
    False
    >>> np.issubdtype(np.float32, np.float64)
    False

    but both are subtypes of `floating`:

    >>> np.issubdtype(np.float64, np.floating)
    True
    >>> np.issubdtype(np.float32, np.floating)
    True

    For convenience, dtype-like objects are allowed too:

    >>> np.issubdtype('S1', np.bytes_)
    True
    >>> np.issubdtype('i4', np.signedinteger)
    True

    """
    if not issubclass_(arg1, generic):
        arg1 = dtype(arg1).type
    if not issubclass_(arg2, generic):
        arg2 = dtype(arg2).type

    return issubclass(arg1, arg2)


def issubdtype(a: DTypeLike | ExtendedDType | None,
               b: DTypeLike | ExtendedDType | None) -> bool:
  """Returns True if first argument is a typecode lower/equal in type hierarchy.

  This is like :func:`numpy.issubdtype`, but can handle dtype extensions such as
  :obj:`jax.dtypes.bfloat16` and `jax.dtypes.prng_key`.
  """
  # Main departures from np.issubdtype are:
  # - "extended" dtypes (like prng key types) are not normal numpy dtypes, so we
  #   need to handle them specifically. However, their scalar types do conform to
  #   the numpy scalar type hierarchy.
  # - custom dtypes (like bfloat16, int4, etc.) are normal numpy dtypes, but they
  #   don't conform to the standard numpy type hierarchy (e.g. the bfloat16 scalar
  #   type is not a subclass of np.floating) so we must also handle these specially.

  # We cannot use the cached version directly for all inputs, because some may be
  # unhashable (e.g. custom objects with a dtype attribute). The following check is
  # fast and covers the majority of calls to this function within JAX library code.
  return _issubdtype_cached(
      a if isinstance(a, _types_for_issubdtype) else np.dtype(a),
      b if isinstance(b, _types_for_issubdtype) else np.dtype(b),
  )


def issubdtype(arg1: DTypeLike, arg2: DTypeLike) -> bool:
  """Return True if arg1 is equal or lower than arg2 in the type hierarchy.

  JAX implementation of :func:`numpy.issubdtype`.

  The main difference in JAX's implementation is that it properly handles
  dtype extensions such as :code:`bfloat16`.

  Args:
    arg1: dtype-like object. In typical usage, this will be a dtype specifier,
      such as ``"float32"`` (i.e. a string), ``np.dtype('int32')`` (i.e. an
      instance of :class:`numpy.dtype`), ``jnp.complex64`` (i.e. a JAX scalar
      constructor), or ``np.uint8`` (i.e. a NumPy scalar type).
    arg2: dtype-like object. In typical usage, this will be a generic scalar
      type, such as ``jnp.integer``, ``jnp.floating``, or ``jnp.complexfloating``.

  Returns:
    True if arg1 represents a dtype that is equal or lower in the type
    hierarchy than arg2.

  See also:
    - :func:`jax.numpy.isdtype`: similar function aligning with the array API standard.

  Examples:
    >>> jnp.issubdtype('uint32', jnp.unsignedinteger)
    True
    >>> jnp.issubdtype(np.int32, jnp.integer)
    True
    >>> jnp.issubdtype(jnp.bfloat16, jnp.floating)
    True
    >>> jnp.issubdtype(np.dtype('complex64'), jnp.complexfloating)
    True
    >>> jnp.issubdtype('complex64', jnp.integer)
    False

    Be aware that while this is very similar to :func:`numpy.issubdtype`, the
    results of these differ in the case of JAX's custom floating point types:

    >>> np.issubdtype('bfloat16', np.floating)
    False
    >>> jnp.issubdtype('bfloat16', jnp.floating)
    True
  """
  return dtypes.issubdtype(arg1, arg2)

