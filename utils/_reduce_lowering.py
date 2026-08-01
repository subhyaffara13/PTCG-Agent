
def _reduce_lowering(body, ctx: LoweringRuleContext, a, *, axes, **kwargs):
  assert isinstance(axes, tuple)
  if not axes:
    return a
  while len(axes) > 1:
    axis = max(axes)
    dst_avals = tuple(v.update(shape=v.shape[:axis] + v.shape[axis + 1:])
                      for v in ctx.avals_in)
    a = _reduce_lowering(
        body, ctx.replace(avals_out=dst_avals), a, axes=(axis,))
    # Adding an intervening -(-reduce(.)) introduces a convert_layout between
    # reduces, which seems necessary for correctness.
    # TODO(bjp): Get rid of the double negation.
    #     https://github.com/openai/triton/issues/1776
    a = _minus(_minus(a))
    ctx = ctx.replace(avals_in=dst_avals)
    axes = tuple(ax for ax in axes if ax != axis)
  return _reduction_lowering(body, ctx, a, axes=axes)[0]

