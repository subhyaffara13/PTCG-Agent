import logging

def _log_array_info(name: str, arr: jax.Array):
  logging.info(
      '%s: shape=%s, dtype=%s, sharding=%s',
      name,
      arr.shape,
      arr.dtype,
      arr.sharding,
  )

