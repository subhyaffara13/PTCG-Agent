
def is_shardable_array(x: ...) -> bool:
  """Returns True if x is a concrete shardable array."""
  return isinstance(x, jax.Array)

