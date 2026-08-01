
def _iota_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    dtype: jnp.dtype,
    dimension: int,
    shape: tuple[int, ...],
    sharding: jax.sharding.Sharding,
):
  del ctx, sharding, dtype, shape
  if block_transform.block_shape[dimension] is None:
    raise ValueError(
        f'Cannot pull iota along dimension {dimension} with None block size.'
    )
  return []

