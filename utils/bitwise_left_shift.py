
def bitwise_left_shift(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.shift_left(a, b)


def bitwise_left_shift(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.left_shift`."""
  return lax.shift_left(*promote_args_numeric("bitwise_left_shift", x, y))

