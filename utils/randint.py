from typing import Any

def randint(
    high: int,
    size: list[int | torch.SymInt],
    **kwargs: Any,
) -> torch.Tensor:
    return aten.randint.low(0, high, size, **kwargs)


def randint(low, high=None, size=None):
    if size is None:
        size = ()
    if not isinstance(size, (tuple, list)):
        size = (size,)
    if high is None:
        low, high = 0, low
    values = torch.randint(low, high, size=size)
    return array_or_scalar(values, int, return_scalar=size == ())


def randint(seed, offset, n_rounds=PHILOX_N_ROUNDS_DEFAULT):
    ret, _, _, _ = randint4x(seed, offset, n_rounds)
    return ret


def randint(g: jit_utils.GraphContext, low, high, shapes, dtype, *options):
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    low_i = symbolic_helper._get_const(low, "i", "low")
    high_i = symbolic_helper._get_const(high, "i", "high")
    if dtype is None:
        scalar_type = _type_utils.JitScalarType.INT64
    else:
        scalar_type = _type_utils.JitScalarType(dtype)
    if low_i is None:
        raise symbolic_helper._onnx_unsupported("randint", low)
    if high_i is None:
        raise symbolic_helper._onnx_unsupported("randint", high)

    shape = symbolic_helper._maybe_get_const(shapes, "is")
    if symbolic_helper._is_value(shape):
        shape_const = g.op(
            "ConstantOfShape",
            shapes,
            value_t=torch.tensor([0], dtype=torch.float),
        )
        randn = g.op(
            "RandomUniformLike",
            shape_const,
            low_f=low_i,
            high_f=high_i,
        )
    else:
        randn = g.op(
            "RandomUniform",
            shape_i=shape,
            low_f=low_i,
            high_f=high_i,
        )

    # cast to integer type
    int_dtype = _type_utils.JitScalarType.INT64
    randint = g.op("Cast", randn, to_i=int_dtype.onnx_type())
    if int_dtype != scalar_type:
        randint = g.op("Cast", randint, to_i=scalar_type.onnx_type())
    return randint


def randint(key: ArrayLike,
            shape: Shape,
            minval: IntegerArray,
            maxval: IntegerArray,
            dtype: DTypeLikeInt | None = None,
            *,
            out_sharding: NamedSharding | P | None = None) -> Array:
  """Sample uniform random values in [minval, maxval) with given shape/dtype.

  Args:
    key: a PRNG key used as the random key.
    shape: a tuple of nonnegative integers representing the shape.
    minval: int or array of ints broadcast-compatible with ``shape``, a minimum
      (inclusive) value for the range.
    maxval: int or array of ints broadcast-compatible with ``shape``, a maximum
      (exclusive) value for the range.
    dtype: optional, an int dtype for the returned values (default int64 if
      jax_enable_x64 is true, otherwise int32).
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with the specified shape and dtype.

  .. note::

     :func:`randint` uses a modulus-based computation that is known to produce
     slightly biased values in some cases. The magnitude of the bias scales as
     ``(maxval - minval) * ((2 ** nbits ) % (maxval - minval)) / 2 ** nbits``:
     in words, the bias goes to zero when ``(maxval - minval)`` is a power of 2,
     and otherwise the bias will be small whenever ``(maxval - minval)`` is
     small compared to the range of the sampled type.

     To reduce this bias, 8-bit and 16-bit values will always be sampled at 32-bit and
     then cast to the requested type. If you find yourself sampling values for which
     this bias may be problematic, a possible alternative is to sample via uniform::

       def randint_via_uniform(key, shape, minval, maxval, dtype):
         u = jax.random.uniform(key, shape, minval=minval - 0.5, maxval=maxval - 0.5)
         return u.round().astype(dtype)

     But keep in mind this method has its own biases due to floating point rounding
     errors, and in particular there may be some integers in the range
     ``[minval, maxval)`` that are impossible to produce with this approach.
  """
  key, _ = _check_prng_key("randint", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      int if dtype is None else dtype)
  shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "randint", shape)

  if not dtypes.issubdtype(dtype, np.integer):
    raise TypeError(f"randint only accepts integer dtypes, got {dtype}")

  info = dtypes.iinfo(dtype)
  dtype_for_sampling = dtype
  if info.bits < 32:
    # Sample in 32 bits to avoid biased results.
    dtype_for_sampling = np.dtype('int32')
    minval = jnp.asarray(minval).astype('int32').clip(int(info.min), int(info.max))
    maxval = jnp.asarray(maxval).astype('int32').clip(int(info.min), int(info.max) + 1)

  return maybe_auto_axes(_randint, out_sharding, shape=shape, dtype=dtype_for_sampling)(
      key, minval, maxval).astype(dtype)

