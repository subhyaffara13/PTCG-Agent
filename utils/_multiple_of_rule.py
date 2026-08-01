
def _multiple_of_rule(ctx: LoweringRuleContext, x, values: Sequence[int]):
  [x_aval] = ctx.avals_in
  assert max(1, len(x_aval.shape)) == len(values)
  _set_attr(
      x,
      "tt.divisibility",
      ir.DenseIntElementsAttr.get(np.asarray(values, dtype=np.int32)),
  )
  return x

