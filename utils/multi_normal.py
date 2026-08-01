
def multi_normal(
    loc: jax.typing.ArrayLike, log_scale: jax.typing.ArrayLike
) -> MultiNormalDiagFromLogScale:
  return MultiNormalDiagFromLogScale(loc=loc, log_scale=log_scale)

