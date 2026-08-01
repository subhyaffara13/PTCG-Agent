
def igammac(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.igammac(a, b)


def igammac(a: ArrayLike, x: ArrayLike) -> Array:
  r"""Elementwise complementary regularized incomplete gamma function."""
  a, x = core.auto_insert_reshard(a, x)
  return igammac_p.bind(a, x)

