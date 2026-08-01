
def _threefry_split_original(key, shape) -> typing.Array:
  num = math.prod(shape)
  counts = lax.iota(np.uint32, num * 2)
  return lax.reshape(threefry_2x32(key, counts), (*shape, 2))

