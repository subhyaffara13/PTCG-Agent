
def _broadcast_to_impl(a, *, shape):
  import jax.numpy as jnp  # pyrefly: ignore[missing-import]
  return jnp.broadcast_to(a, shape)

