
def bitwise_invert(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.invert`."""
  return lax.bitwise_not(*promote_args('bitwise_invert', x))

