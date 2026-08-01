
def _is_host_array(x) -> bool:
  """True if x is a jax.Array on CPU."""
  return isinstance(x, jax.Array) and next(iter(x.devices())).platform == "cpu"


def _is_host_array(x) -> bool:
  """True if x is a jax.Array on CPU."""
  return isinstance(x, jax.Array) and next(iter(x.devices())).platform == "cpu"


def _is_host_array(x) -> bool:
  """True if x is a jax.Array on CPU."""
  return isinstance(x, jax.Array) and next(iter(x.devices())).platform == "cpu"

