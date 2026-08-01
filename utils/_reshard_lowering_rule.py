
def _reshard_lowering_rule(ctx: LoweringRuleContext, x, *, dst_sharding,
                           concrete_mesh):
  return x


def _reshard_lowering_rule(ctx, x, dst_sharding, concrete_mesh):
  del ctx, dst_sharding, concrete_mesh
  return x


def _reshard_lowering_rule(ctx, x, *, dst_sharding, concrete_mesh):
  return x

