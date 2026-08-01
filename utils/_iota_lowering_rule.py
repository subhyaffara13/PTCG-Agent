
def _iota_lowering_rule(ctx: LoweringRuleContext, dtype, shape, dimension,
                        sharding):
  if len(shape) == 1:
    if dimension != 0:
      raise ValueError("Dimension must be 0 for 1D iota.")
    def _1d_iota_helper():
      iota_2d = lax.iota_p.bind(dtype=dtype,
                                shape=(1,) + shape,
                                dimension=1,
                                sharding=sharding)
      return iota_2d[0]
    return lower_fun(_1d_iota_helper)(ctx)
  out_type = ctx.aval_to_ir_type(ctx.avals_out[0])
  return tpu.iota(out_type, dimensions=[dimension])


def _iota_lowering_rule(ctx: LoweringRuleContext, *, dtype, shape, dimension,
                        sharding):
  iota = _make_range(0, shape[dimension])
  iota = _cast(iota, jnp.int32, dtype)
  for i in range(len(shape)):
    if i != dimension:
      iota = _expand_dims(iota, i)
  return _bcast_to(iota, shape)

