
def _bytes(x: jax.Array | jax.ShapeDtypeStruct) -> int:
  return math.prod(x.shape) * x.dtype.itemsize

