
def _bitcast_convert_type_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    new_dtype: jnp.dtype,
):
  old_dtype = ctx.avals_in[0].dtype
  if old_dtype.itemsize != new_dtype.itemsize:
    raise NotImplementedError(
        'bitcast_convert_type with different bitwidths not supported yet:'
        f' {old_dtype=}, {new_dtype=}'
    )
  return [block_transform]

