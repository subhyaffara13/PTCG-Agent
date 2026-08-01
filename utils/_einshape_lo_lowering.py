
def _einshape_lo_lowering(
    ctx: mlir.LoweringRuleContext,
    x,
    *,
    equation: str,
    sizes: tuple[tuple[str, int], ...],
    assert_is_tile_preserving: bool,
):
  del assert_is_tile_preserving

  def f(x):
    return _einshape(equation, x, **dict(sizes))

  return mlir.lower_fun(f, multiple_results=False)(ctx, x)

