
def _argreduce_lowering(
    body, ctx: LoweringRuleContext, a, *, axes, index_dtype
):
  if index_dtype != jnp.int32:
    raise ValueError("`index_type` must be i32.")
  if len(axes) != 1:
    raise ValueError("`pallas` reduce operations only support one reduce axis.")
  [axis] = axes
  [a_aval] = ctx.avals_in
  index = _make_range(0, a_aval.shape[axis])
  if len(a_aval.shape) > 1:
    # Broadcast index across the non-reduced axes
    for i in range(len(a_aval.shape)):
      if i != axis:
        index = _expand_dims(index, i)
    index = _bcast_to(index, a_aval.shape)
  ctx = ctx.replace(avals_in=[a_aval, a_aval.update(dtype=jnp.dtype(jnp.int32))])
  _, indices = _reduction_lowering(body, ctx, (a, index), axes=axes)
  return indices

