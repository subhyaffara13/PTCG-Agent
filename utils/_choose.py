
def _choose(self: Array, choices: Sequence[ArrayLike], out: None = None, mode: str = 'raise') -> Array:
  """Construct an array choosing from elements of multiple arrays.

  Refer to :func:`jax.numpy.choose` for the full documentation.
  """
  return lax_numpy.choose(self, choices=choices, out=out, mode=mode)

