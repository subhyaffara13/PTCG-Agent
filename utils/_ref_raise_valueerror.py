
def _ref_raise_valueerror(*args, **kwargs):
  raise ValueError(
      "Eager shard_map cannot return a `jax.Ref`. Please wrap"
      " your shard_map in `jax.jit`.")

