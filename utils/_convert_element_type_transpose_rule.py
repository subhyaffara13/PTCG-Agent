
def _convert_element_type_transpose_rule(ct, operand, *, new_dtype, weak_type,
                                         sharding):
  assert ad.is_undefined_primal(operand)
  old_dtype = operand.aval.dtype
  old_weak_type = dtypes.is_weakly_typed(operand)
  if type(ct) is ad_util.Zero:
    return [ad_util.Zero(operand.aval)]
  elif core.primal_dtype_to_tangent_dtype(old_dtype) == dtypes.float0:
    return [ad_util.Zero(operand.aval.update(dtype=dtypes.float0, weak_type=False))]
  else:
    out = convert_element_type_p.bind(
        ct, new_dtype=old_dtype, weak_type=old_weak_type,
        sharding=operand.aval.sharding)
    return [out]

