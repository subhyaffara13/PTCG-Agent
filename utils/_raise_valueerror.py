
def _raise_valueerror(name, arg, *, axes):
  raise ValueError(f'{name} should be called under jax.shard_map.')

