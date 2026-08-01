
def ldexp(self: Tensor, other: Tensor) -> Tensor:
    two_dtype = (
        torch.float32
        if utils.is_integer_dtype(self.dtype) or utils.is_boolean_dtype(self.dtype)
        else self.dtype
    )
    two_tensor = self.new_full((), 2.0, dtype=two_dtype)
    return self * torch.pow(two_tensor, other)


def ldexp(
    x1: ArrayLikeOrScalar,
    x2: ArrayLikeOrScalar,
    /,
    out: OutArray | None = None,
    *,
    where: NotImplementedType = True,
    casting: CastingModes | None = "same_kind",
    order: NotImplementedType = "K",
    dtype: DTypeLike | None = None,
    subok: NotImplementedType = False,
    signature: NotImplementedType = None,
    extobj: NotImplementedType = None,
):
    if dtype is not None:
        if isinstance(x1, torch.Tensor):
            x1 = _util.typecast_tensor(x1, dtype, casting)
        else:
            x1 = torch.as_tensor(x1, dtype=dtype)
    else:
        if not isinstance(x1, torch.Tensor):
            x1 = torch.as_tensor(x1)
            x1 = _util.cast_int_to_float(x1)

    x2 = torch.as_tensor(x2)
    # the second arg must be integer
    if _dtypes_impl._category(x2.dtype) != 1:
        raise ValueError("ldexp 2nd arg must be integer")

    result = _binary_ufuncs_impl.ldexp(x1, x2)

    if x1.dtype == torch.float16:
        # torch.ldexp(f16, int) -> f32, undo it
        result = result.to(torch.float16)

    return _ufunc_postprocess(result, out, casting)


def ldexp(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Compute x1 * 2 ** x2

  JAX implementation of :func:`numpy.ldexp`.

  Note that XLA does not provide an ``ldexp`` operation, so this
  is implemneted in JAX via a standard multiplication and
  exponentiation.

  Args:
    x1: real-valued input array.
    x2: integer input array. Must be broadcast-compatible with ``x1``.

  Returns:
    ``x1 * 2 ** x2`` computed element-wise.

  See also:
    - :func:`jax.numpy.frexp`: decompose values into mantissa and exponent.

  Examples:
    >>> x1 = jnp.arange(5.0)
    >>> x2 = 10
    >>> jnp.ldexp(x1, x2)
    Array([   0., 1024., 2048., 3072., 4096.], dtype=float32)

    ``ldexp`` can be used to reconstruct the input to ``frexp``:

    >>> x = jnp.array([2., 3., 5., 11.])
    >>> m, e = jnp.frexp(x)
    >>> m
    Array([0.5   , 0.75  , 0.625 , 0.6875], dtype=float32)
    >>> e
    Array([2, 2, 3, 4], dtype=int32)
    >>> jnp.ldexp(m, e)
    Array([ 2.,  3.,  5., 11.], dtype=float32)
  """
  x1, x2 = ensure_arraylike("ldexp", x1, x2)
  x1_dtype = x1.dtype
  x2_dtype = x2.dtype
  if (dtypes.issubdtype(x1_dtype, np.complexfloating)
      or dtypes.issubdtype(x2_dtype, np.inexact)):
    raise ValueError(f"ldexp not supported for input types {(x1_dtype, x2_dtype)}")
  x1, = promote_args_inexact("ldexp", x1)
  x2 = lax.convert_element_type(x2, x1.dtype)

  # Split off the exponent to avoid overflow for small x1 and large x2.
  m, e = frexp(x1)
  e = (e.astype(x2.dtype) + x2).astype(x1.dtype)

  # exponent may overflow by 1 and still have a finite result.
  m = _where(e > 0, m * 2, m)
  e = _where(e > 0, e - 1, e)

  x = m * (2 ** e.astype(m.dtype))
  return _where(isinf(x1) | (x1 == 0), x1, x)

