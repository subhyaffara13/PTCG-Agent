
def _einshape_kernel(
    equation: str,
    x: jax_typing.Array,
    assert_is_tile_preserving: bool,
    **size_vars: int,
):
  transforms = get_einshape_transforms(equation, x.shape, **dict(size_vars))
  if len(transforms) <= 1:
    return _default_einshape_kernel(equation, x, **size_vars)
  tiling = tpu_info.infer_tiling(jax_core.ShapedArray(x.shape, x.dtype))
  if _is_tile_preserving(x.shape, transforms, tiling[-2:]):  # pyrefly: ignore[bad-argument-type]
    return _tile_preserving_einshape_kernel(equation, x, **size_vars)
  elif assert_is_tile_preserving:
    raise ValueError(
        "Tile preserving check failed for einshape kernel with equation:"
        f" {equation} and shape {x.shape} and tiling {tiling}."
    )
  return _default_einshape_kernel(equation, x, **size_vars)

