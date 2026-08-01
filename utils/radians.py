
def radians(x: float) -> float:
    import math

    return math.pi / 180.0 * x


def radians(ctx, x):
    return x * ctx.degree


def radians(x: ArrayLike, /) -> Array:
  """Alias of :func:`jax.numpy.deg2rad`"""
  return deg2rad(x)

