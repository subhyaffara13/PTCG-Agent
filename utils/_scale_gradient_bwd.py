
def _scale_gradient_bwd(
    scale: jax.typing.ArrayLike, g: base.ArrayTree
) -> tuple[base.ArrayTree, None]:
  return (jax.tree.map(lambda g_: g_ * scale, g), None)

