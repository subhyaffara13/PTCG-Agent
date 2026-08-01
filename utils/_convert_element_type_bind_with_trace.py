
def _convert_element_type_bind_with_trace(trace, args, avals, params):
  sharding = params['sharding']
  operand = core.Primitive.bind_with_trace(convert_element_type_p, trace, args,
                                           avals, params)
  if sharding is not None and sharding._is_concrete:
    with core.set_current_trace(trace):
      operand = pjit.with_sharding_constraint(operand, sharding)
  return operand

