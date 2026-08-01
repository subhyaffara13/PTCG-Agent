
def clz(x):
  assert np.issubdtype(x.dtype, np.integer)
  nbits = np.iinfo(x.dtype).bits
  mask = (2 ** np.arange(nbits, dtype=x.dtype))[::-1]
  bits = (x[..., None] & mask).astype(np.bool_)
  out = np.argmax(bits, axis=-1).astype(x.dtype)
  out[x == 0] = nbits
  return out


def clz(x: ArrayLike) -> Array:
  r"""Elementwise count-leading-zeros.

  This function lowers directly to the `stablehlo.count_leading_zeros`_ operation.

  Args:
    x: Input array. Must have integer dtype.

  Returns:
    An array of the same shape and dtype as ``x``, containing the number of
    leading zeros in the input.

  See also:
    - :func:`jax.lax.population_count`: Count the number of set bits in each element.

  .. _stablehlo.count_leading_zeros: https://openxla.org/stablehlo/spec#count_leading_zeros
  """
  return clz_p.bind(x)

