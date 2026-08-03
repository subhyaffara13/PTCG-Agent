import functools

def _einshape_lo_abstract_eval(
    x_aval: jax_core.ShapedArray,
    *,
    equation: str,
    sizes: tuple[tuple[str, int], ...],
    assert_is_tile_preserving: bool,
):
  del assert_is_tile_preserving
  out_sds = api.eval_shape(
      functools.partial(_einshape, equation, **dict(sizes)), x_aval
  )
  return x_aval.update(shape=out_sds.shape, dtype=out_sds.dtype)

