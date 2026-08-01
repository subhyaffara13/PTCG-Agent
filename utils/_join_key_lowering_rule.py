
def _join_key_lowering_rule(ctx: LoweringRuleContext, *scalars, impl):
  if not pl_random.is_pallas_impl(impl):
    return ValueError(f"Can only join Pallas keys. Got impl={impl}")
  return KeyScalarBundle(scalars=scalars, key_shape=tuple(impl.key_shape))

