
def _scale_gradient_fwd(
    inputs: base.ArrayTree, scale: jax.typing.ArrayLike
) -> tuple[base.ArrayTree, jax.typing.ArrayLike]:
  return _scale_gradient(inputs, scale), scale

