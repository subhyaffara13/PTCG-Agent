
def bitwise_right_shift(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.shift_right_arithmetic(a, b)


def bitwise_right_shift(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.right_shift`."""
  return right_shift(x1, x2)

