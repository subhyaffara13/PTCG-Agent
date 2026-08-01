
def align_to(a: int, alignment: int) -> int:
  ...


def align_to(a: int, alignment: jax_typing.Array) -> jax_typing.Array:
  ...


def align_to(a: jax_typing.Array, alignment: int) -> jax_typing.Array:
  ...


def align_to(a: jax_typing.Array, alignment: jax_typing.Array) -> jax_typing.Array:
  ...


def align_to(
    a: int | jax_typing.Array, alignment: int | jax_typing.Array
) -> int | jax_typing.Array:
  """Rounds ``a`` up to the nearest multiple of ``alignment``.

  Examples:
    >>> align_to(8, 4)
    8
    >>> align_to(5, 4)  # 5 is not a multiple of 4, so rounds up to 8
    8
  """
  return cdiv(a, alignment) * alignment


def align_to(x: int, alignment: int):
  if rem := x % alignment:
    return x + alignment - rem
  return x

