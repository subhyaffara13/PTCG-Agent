
def _convert_element_type_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    new_dtype: jnp.dtype,
    weak_type: bool,
    sharding: jax.sharding.Sharding,
):
  del ctx, new_dtype, weak_type, sharding
  return [block_transform]

