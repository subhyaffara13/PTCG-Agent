
def _max_contiguous_rule(
    ctx: lowering.LoweringRuleContext, x, values: Sequence[int]
):
  [x_aval] = ctx.avals_in
  assert len(x_aval.shape) == len(values)
  lowering._set_attr(
      x,
      "tt.contiguity",
      ir.DenseIntElementsAttr.get(np.asarray(values, dtype=np.int32)),
  )
  return x

