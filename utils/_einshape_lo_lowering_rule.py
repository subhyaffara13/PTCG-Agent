
def _einshape_lo_lowering_rule(
    ctx: tpu_lowering.LoweringRuleContext,
    x,
    *,
    equation: str,
    sizes: tuple[tuple[str, int], ...],
    assert_is_tile_preserving: bool,
):
  return tpu_lowering.lower_fun(
      lambda x: _einshape_kernel(
          equation,
          x,
          assert_is_tile_preserving=assert_is_tile_preserving,
          **dict(sizes),
      ),
  )(ctx, x)

