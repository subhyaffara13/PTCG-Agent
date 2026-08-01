
def igamma(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.igamma(a, b)


def igamma(a: ArrayLike, x: ArrayLike) -> Array:
  r"""Elementwise regularized incomplete gamma function."""
  a, x = core.auto_insert_reshard(a, x)
  return igamma_p.bind(a, x)

