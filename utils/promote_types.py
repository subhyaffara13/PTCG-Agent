
def promote_types(
    args: Sequence[DTypeArg],
    type_promotion_kind: ELEMENTWISE_TYPE_PROMOTION_KIND | None = None,
):
    dtype_prop_candidates = []

    for arg in args:
        assert not isinstance(arg, str)
        if isinstance(arg, OpsValue):
            arg = arg.value
            assert isinstance(arg, torch._prims_common.Number) or hasattr(arg, "dtype")

        if isinstance(arg, torch._prims_common.Number):
            dtype_prop_candidates.append((type_to_dtype(type(arg)), True))
            continue

        # pyrefly: ignore [missing-attribute]
        dtype_prop_candidates.append((arg.dtype, getattr(arg, "is_scalar", False)))

    dtype = get_promoted_dtype(
        *dtype_prop_candidates,
        type_promotion_kind=type_promotion_kind,
    )

    return dtype


def promote_types(a: DTypeLike, b: DTypeLike) -> DType:
  """Returns the type to which a binary operation should cast its arguments.

  JAX implementation of :func:`numpy.promote_types`. For details of JAX's
  type promotion semantics, see :ref:`type-promotion`.

  Args:
    a: a :class:`numpy.dtype` or a dtype specifier.
    b: a :class:`numpy.dtype` or a dtype specifier.

  Returns:
    A :class:`numpy.dtype` object.

  Examples:
    Type specifiers may be strings, dtypes, or scalar types, and the return
    value is always a dtype:

    >>> jnp.promote_types('int32', 'float32')  # strings
    dtype('float32')
    >>> jnp.promote_types(jnp.dtype('int32'), jnp.dtype('float32'))  # dtypes
    dtype('float32')
    >>> jnp.promote_types(jnp.int32, jnp.float32)  # scalar types
    dtype('float32')

    Built-in scalar types (:type:`int`, :type:`float`, or :type:`complex`) are
    treated as weakly-typed and will not change the bit width of a strongly-typed
    counterpart (see discussion in :ref:`type-promotion`):

    >>> jnp.promote_types('uint8', int)
    dtype('uint8')
    >>> jnp.promote_types('float16', float)
    dtype('float16')

    This differs from the NumPy version of this function, which treats built-in scalar
    types as equivalent to 64-bit types:

    >>> import numpy
    >>> numpy.promote_types('uint8', int)
    dtype('int64')
    >>> numpy.promote_types('float16', float)
    dtype('float64')
  """
  # Note: we deliberately avoid `if a in _weak_types` here because we want to check
  # object identity, not object equality, due to the behavior of np.dtype.__eq__
  a_tp = cast(JAXType, a if any(a is t for t in _weak_types) else np.dtype(a))
  b_tp = cast(JAXType, b if any(b is t for t in _weak_types) else np.dtype(b))
  return np.dtype(_least_upper_bound(
      config.numpy_dtype_promotion.value, config.enable_x64.value, a_tp, b_tp))

