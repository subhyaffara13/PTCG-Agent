from typing import Any

def create_pytree() -> dict[str, Any]:
  return {
      'a': jnp.array([0, 1, 2, 3, 4, 5, 6, 7], dtype=jnp.int32),
      'b': {'c': jnp.array([1, 2, 3], dtype=jnp.int32)},
  }


def create_pytree() -> dict[str, Any]:
  return {
      'a': jnp.array([0, 1, 2, 3, 4, 5, 6, 7], dtype=jnp.int32),
      'b': {'c': jnp.array([1, 2, 3], dtype=jnp.int32)},
  }

