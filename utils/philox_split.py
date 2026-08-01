
def philox_split(key, shape: Shape):
  """Splits the key into two keys of the same shape."""
  bits1, bits2 = philox_4x32_count(key, shape, fuse_output=False)
  return jnp.stack([bits1, bits2], axis=bits1.ndim)

