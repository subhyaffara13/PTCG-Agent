
def _sort_lowering_rule(
    ctx: LoweringRuleContext, *xs, dimension, is_stable, num_keys
):
  del is_stable  # Unused, always stable.
  if dimension not in (0, -1):
    raise ValueError(f"Unsupported dimension: {dimension}")
  if num_keys != 1:
    raise NotImplementedError("Multiple sort keys not supported")
  sc_info = sc_core.get_sparse_core_info()
  supported_shape = (sc_info.num_lanes,)
  for i, aval in enumerate(ctx.avals_in):
    if aval.shape != supported_shape:
      raise NotImplementedError(
          f"Unsupported shape for operand {i} of SC sort: Got {aval.shape}, "
          f"expected {supported_shape}"
      )
  keys = xs[0]
  values = xs[1:]
  mask_type = ir.VectorType.get(
      [sc_info.num_lanes], ir.IntegerType.get_signless(1))
  mask = arith.constant(mask_type, ir.DenseElementsAttr.get_splat(
      mask_type, ir.BoolAttr.get(True)))
  if not values:
    _, sorted_keys, _ = tpu.sort(
        mask_type, keys.type, keys.type, keys, keys, mask=mask
    )
    return (sorted_keys,)
  results: list[ir.Value] = []
  for value in values:
    _, sorted_keys, sorted_value = tpu.sort(
        mask_type, keys.type, value.type, keys, value, mask=mask
    )
    if not results:
      results.append(sorted_keys)
    results.append(sorted_value)
  return tuple(results)

