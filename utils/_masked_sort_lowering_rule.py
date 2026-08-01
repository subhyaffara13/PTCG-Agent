
def _masked_sort_lowering_rule(
    ctx: sc_lowering.LoweringRuleContext, keys, values, *maybe_mask, descending):
  if maybe_mask:
    [mask] = maybe_mask
  else:
    mask_type = ir.VectorType.get(
        [sc_core.get_sparse_core_info().num_lanes],
        ir.IntegerType.get_signless(1))
    mask = arith.constant(mask_type, ir.DenseElementsAttr.get_splat(
        mask_type, ir.BoolAttr.get(True)))
  # tpu.sort comparisons assume unsigned int predicates, so we sort
  # with the sign bit flipped to get correct signed int32 ordering.
  sign_bit_vec = None
  if ctx.avals_in[0].dtype == jnp.dtype(jnp.int32):
    i32 = ir.IntegerType.get_signless(32)
    sign_bit_vec = vector.broadcast(
        keys.type, arith.constant(i32, ir.IntegerAttr.get(i32, 0x80000000)))
    keys = arith.xori(keys, sign_bit_vec)
  out_mask, sorted_keys, sorted_values = tpu.sort(
      mask.type, keys.type, values.type, keys, values, mask=mask,
      descending=descending
  )
  if sign_bit_vec is not None:
    sorted_keys = arith.xori(sorted_keys, sign_bit_vec)
  if maybe_mask:
    return sorted_keys, sorted_values, out_mask
  return sorted_keys, sorted_values

