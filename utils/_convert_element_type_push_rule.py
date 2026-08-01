
def _convert_element_type_push_rule(
    ctx: PushRuleContext,
    block_spec: pallas_core.BlockSpec,
    *,
    new_dtype: jnp.dtype,
    weak_type: bool,
    sharding: jax.sharding.Sharding,
):
  del ctx, new_dtype, weak_type, sharding
  return block_spec

