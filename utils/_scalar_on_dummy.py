from typing import Any

def _scalar_on_dummy(
    value: Any, dummy: jax.Array, *, dtype: Any
) -> jax.Array:
  return jax.device_put(jnp.asarray(value, dtype=dtype), dummy.sharding)

