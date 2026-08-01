
def _iota_lowering_rule_sc(ctx: LoweringRuleContext, dtype, shape, dimension,
                           sharding):
  sc_info = sc_core.get_sparse_core_info()
  if shape != (sc_info.num_lanes,):
    raise ValueError(
        f"Unsupported iota shape for SC vector subcore. Got {shape}, supported "
        f"shape is {(sc_info.num_lanes,)}."
    )
  [out_aval] = ctx.avals_out
  out_type = ir.VectorType.get(
      [sc_info.num_lanes], _dtype_to_ir_type(out_aval.dtype)
  )
  return tpu.iota(out_type, dimensions=[dimension])

