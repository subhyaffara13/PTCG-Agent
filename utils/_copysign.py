
def _copysign(x1: jax.typing.ArrayLike, x2: jax.typing.ArrayLike) -> jax.Array:
  return _copysign_p.bind(x1, x2)

