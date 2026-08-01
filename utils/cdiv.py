
def cdiv(a: int, b: int) -> int:
  ...


def cdiv(a: int, b: jax_typing.Array) -> jax_typing.Array:
  ...


def cdiv(a: jax_typing.Array, b: int) -> jax_typing.Array:
  ...


def cdiv(a: jax_typing.Array, b: jax_typing.Array) -> jax_typing.Array:
  ...


def cdiv(a: int | jax_typing.Array, b: int | jax_typing.Array) -> int | jax_typing.Array:
  """Computes the ceiling division of a divided by b.

  Examples:
    >>> cdiv(8, 2)
    4
    >>> cdiv(9, 2)  # 9 / 2 = 4.5, which rounds up to 5
    5
  """
  if jax_core.is_dim(a) and jax_core.is_dim(b):
    return (a + b - 1) // b
  return lax.div(a + (b - 1), b)

