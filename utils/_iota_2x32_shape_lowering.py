
def _iota_2x32_shape_lowering(ctx: LoweringRuleContext, *, shape):
  total_elements = math.prod(shape)
  if total_elements > np.iinfo(jnp.int32).max:
    raise NotImplementedError(f"Iota with >{np.iinfo(jnp.int32).max} items.")

  def _lower_fun(shape):
    iota_data = jnp.zeros(shape, dtype=jnp.int32)
    multiplier = 1
    for dim in range(len(shape)-1, -1, -1):
      counts_lo = lax.broadcasted_iota(
          dtype=jnp.int32, shape=shape, dimension=dim
      )
      iota_data += counts_lo * multiplier
      multiplier *= shape[dim]
    counts_hi = jnp.zeros(shape, dtype=jnp.int32)
    return counts_hi, iota_data

  iota_lowering = lower_fun(_lower_fun)
  return iota_lowering(ctx, shape=shape)

