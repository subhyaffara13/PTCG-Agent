
def _reduce_lowering_rule_wg(
    ctx: LoweringRuleContext,
    kind: vector_dialect.CombiningKind,
    acc: int | float,
    x,
    axes,
) -> ir.Value:
  [x_aval] = ctx.avals_in
  [out_aval] = ctx.avals_out
  x = _ensure_ir_value(x, x_aval.dtype)
  out_type = mgpu_utils.dtype_to_ir_type(out_aval.dtype)
  if not out_aval.shape:
    # Special-case: reducing to a scalar.
    if x_aval.ndim != 1:
      # Flatten to 1D, since vector.reduction only supports 1D inputs.
      x = vector_dialect.shape_cast(
          ir.VectorType.get([x_aval.size], out_type), x
      )
    reduction = vector_dialect.ReductionOp(out_type, kind, x)
  else:
    acc_vec = vector_dialect.broadcast(
        ir.VectorType.get(out_aval.shape, out_type),
        _ensure_ir_value(acc, out_aval.dtype),
    )
    reduction = vector_dialect.MultiDimReductionOp(kind, x, acc_vec, axes)
  def i32_attr(value: int) -> ir.IntegerAttr:
    return ir.IntegerAttr.get(ir.IntegerType.get_signless(32), value)
  reduction.attributes["offset"] = i32_attr(ctx.module_ctx.smem_used_bytes)
  # TODO(bchetioui): here, we could just donate all the remaining free SMEM that
  # we have at this point in time.
  reduction.attributes["scratch_size"] = i32_attr(ctx.module_ctx.reduction_scratch_bytes)
  return reduction.result

