
def _rand_dtype(rand, shape, dtype, scale=1., post=lambda x: x):
  """Produce random values given shape, dtype, scale, and post-processor.

  Args:
    rand: a function for producing random values of a given shape, e.g. a
      bound version of either np.RandomState.randn or np.RandomState.rand.
    shape: a shape value as a tuple of positive integers.
    dtype: a numpy dtype.
    scale: optional, a multiplicative scale for the random values (default 1).
    post: optional, a callable for post-processing the random values (default
      identity).

  Returns:
    An ndarray of the given shape and dtype using random values based on a call
    to rand but scaled, converted to the appropriate dtype, and post-processed.
  """
  if _dtypes.issubdtype(dtype, np.unsignedinteger):
    r = lambda: np.asarray(scale * abs(rand(*_dims_of_shape(shape)))).astype(dtype)
  else:
    r = lambda: np.asarray(scale * rand(*_dims_of_shape(shape))).astype(dtype)
  if _dtypes.issubdtype(dtype, np.complexfloating):
    vals = r() + 1.0j * r()
  else:
    vals = r()
  return _cast_to_shape(np.asarray(post(vals), dtype), shape, dtype)

