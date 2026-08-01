
def _broadcast_to_lowering_rule(
    ctx: LoweringRuleContext, x, shape: Sequence[int]
):
  raise RuntimeError(
      "`broadcast_to` is a Triton-specific primitive. Please consider using"
      " `jnp.broadcast_to` instead."
  )

