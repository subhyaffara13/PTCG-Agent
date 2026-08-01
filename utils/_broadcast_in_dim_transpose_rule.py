
def _broadcast_in_dim_transpose_rule(ct, operand,
                                     shape, broadcast_dimensions, sharding):
  if not isinstance(operand, ad.UndefinedPrimal):
    return [None]  # transpose wrt literal
  if type(ct) is ad_util.Zero:
    return [ad_util.Zero(operand.aval)]
  ct_s = operand.aval.sharding
  unit_dims = [
      i for i, (sh, spec) in enumerate(zip(operand.aval.shape, ct_s.spec.partitions))
      if core.definitely_equal(sh, 1) and spec is None
  ]
  bdims = tuple_delete(broadcast_dimensions, unit_dims)
  axes = tuple_delete(tuple(range(len(shape))), bdims)
  ct_s = ct_s.update(spec=ct_s.spec.update(
      partitions=tuple_delete(ct_s.spec.partitions, unit_dims)))
  return [expand_dims(reduce_sum(ct, axes, out_sharding=ct_s), unit_dims)]

