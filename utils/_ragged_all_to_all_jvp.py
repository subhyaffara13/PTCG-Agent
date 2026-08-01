
def _ragged_all_to_all_jvp(primals, tangents, **params):
  operand, output, *sizes_and_offsets = primals
  operand_dot, output_dot, *_ = tangents
  result = ragged_all_to_all_p.bind(
      operand, output, *sizes_and_offsets, **params)
  if type(operand_dot) is type(output_dot) is ad.Zero:
    result_dot = ad.p2tz(result)
  else:
    operand_dot = ad.instantiate_zeros(operand_dot)
    output_dot = ad.instantiate_zeros(output_dot)
    result_dot = ragged_all_to_all_p.bind(
        operand_dot, output_dot, *sizes_and_offsets, **params)
  return result, result_dot

