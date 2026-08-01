
def _view(self: Array, dtype: DTypeLike | None = None, type: None = None) -> Array:
  """Return a bitwise copy of the array, viewed as a new dtype.

  This is fuller-featured wrapper around :func:`jax.lax.bitcast_convert_type`.

  If the source and target dtype have the same bitwidth, the result has the same
  shape as the input array. If the bitwidth of the target dtype is different
  from the source, the size of the last axis of the result is adjusted
  accordingly.

  >>> jnp.zeros([1,2,3], dtype=jnp.int16).view(jnp.int8).shape
  (1, 2, 6)
  >>> jnp.zeros([1,2,4], dtype=jnp.int8).view(jnp.int16).shape
  (1, 2, 2)

  Conversions involving booleans are not well-defined in all situations. With
  regards to the shape of result as explained above, booleans are treated as
  having a bitwidth of 8. However, when converting to a boolean array, the input
  should only contain 0 or 1 bytes. Otherwise, results may be unpredictable or
  may change depending on how the result is used.

  This conversion is guaranteed and safe::

    >>> jnp.array([1, 0, 1], dtype=jnp.int8).view(jnp.bool_)
    Array([ True, False,  True], dtype=bool)

  However, there are no guarantees about the results of any expression involving
  a view such as this: ``jnp.array([1, 2, 3], dtype=jnp.int8).view(jnp.bool_)``.
  In particular, the results may change between JAX releases and depending on
  the platform. To safely convert such an array to a boolean array, compare it
  with `0`::

    >>> jnp.array([1, 2, 0], dtype=jnp.int8) != 0
    Array([ True,  True, False], dtype=bool)

  Args:
    dtype: An optional output dtype. If not specified, the output dtype is the
      same as the input dtype.
    type: Not implemented; accepted for NumPy compatibility.
  Returns:
    The array, viewed as the new dtype. Unlike NumPy, the array may or may not
    be a copy of the input array.
  """
  if type is not None:
    raise NotImplementedError("`type` argument of array.view() is not supported.")

  if dtype is None:
    return self

  dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "view")

  nbits_in = dtypes.itemsize_bits(self.dtype)
  nbits_out = dtypes.itemsize_bits(dtype)

  if self.ndim == 0:
    if nbits_in != nbits_out:
      raise ValueError("view() of a 0d array is only supported if the itemsize is unchanged.")
    return _view(lax.expand_dims(self, (0,)), dtype).squeeze()

  if (self.shape[-1] * nbits_in) % nbits_out != 0:
    raise ValueError("When changing to a larger dtype, its size must be a divisor "
                     "of the total size in bytes of the last axis of the array.")

  if self.dtype == dtype:
    return self

  # lax.bitcast_convert_type does not support bool or complex; in these cases we
  # cast to a compatible type and recursively call _view for simplicity.
  if self.dtype == bool:
    return _view(self.astype('uint8'), dtype)

  if lax_numpy.issubdtype(self.dtype, np.complexfloating):
    new_shape = (*self.shape[:-1], self.shape[-1] * 2)
    new_dtype = lax_numpy.finfo(self.dtype).dtype
    new_sharding = core.typeof(self).sharding
    self = (array_creation.zeros(new_shape, new_dtype, out_sharding=new_sharding)
            .at[..., 0::2].set(self.real)
            .at[..., 1::2].set(self.imag))
    return _view(self, dtype)

  if dtype == bool:
    return _view(self, np.uint8).astype(bool)

  if lax_numpy.issubdtype(dtype, np.complexfloating):
    out = _view(self, lax_numpy.finfo(dtype).dtype).astype(dtype)
    return out[..., 0::2] + 1j * out[..., 1::2]

  # lax.bitcast_convert_type adds or subtracts dimensions depending on the
  # relative bitwidths of the dtypes; we account for that with reshapes.
  if nbits_in < nbits_out:
    factor = nbits_out // nbits_in
    out = self.reshape(*self.shape[:-1], self.shape[-1] // factor, factor)
    return lax.bitcast_convert_type(out, dtype)
  elif nbits_in > nbits_out:
    out = lax.bitcast_convert_type(self, dtype)
    return out.reshape(*out.shape[:-2], out.shape[-2] * out.shape[-1])
  else:
    return lax.bitcast_convert_type(self, dtype)

