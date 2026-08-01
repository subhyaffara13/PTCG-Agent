
def _byteswap(self: Array) -> Array:
  """Swap the bytes of the array elements.

  This switches between a little-endian and big-endian data
  representation.

  Returns:
    An array with the same dtype as ``self``, with underlying bytes of each
    entry reversed.

  Examples:
    >>> import jax.numpy as jnp
    >>> x = jnp.arange(5, dtype='int32')
    >>> x
    Array([0, 1, 2, 3, 4], dtype=int32)
    >>> x.byteswap()
    Array([       0, 16777216, 33554432, 50331648, 67108864], dtype=int32)

    When the resulting bytes are viewed as a big-endian dtype (possible in NumPy,
    but not in JAX) they represent the original values:

    >>> import numpy as np
    >>> np.array(x.byteswap()).view('>i4')  # view as big-endian
    array([0, 1, 2, 3, 4], dtype='>i4')

    Calling byteswap twice will return the original array:

    >>> x.byteswap().byteswap()
    Array([0, 1, 2, 3, 4], dtype=int32)
  """
  if dtypes.issubdtype(self.dtype, np.complexfloating):
    return lax.complex(self.real.byteswap(), self.imag.byteswap())
  if self.itemsize == 1:
    return self.copy()
  bytes_original = lax.bitcast_convert_type(self, np.dtype('uint8'))
  bytes_swapped = lax.rev(bytes_original, [self.ndim])
  return lax.bitcast_convert_type(bytes_swapped, self.dtype)

