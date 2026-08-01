
def _convert_element_type_jvp_rule(tangent, primal_result, operand, *,
                                   new_dtype, weak_type, sharding):
  new_tangent_dtype = core.primal_dtype_to_tangent_dtype(new_dtype)
  if new_tangent_dtype == dtypes.float0:
    return ad_util.p2tz(primal_result)
  else:
    return convert_element_type_p.bind(tangent, new_dtype=new_tangent_dtype,
                                       weak_type=weak_type, sharding=sharding)

