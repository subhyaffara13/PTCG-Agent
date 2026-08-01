
def _approx_top_k_jvp(primals, tangents, *, k, reduction_dimension,
                      recall_target, is_max_k, reduction_input_size_override,
                      aggregate_to_topk):
  operand, = primals
  tangent, = tangents
  if is_max_k:
    val_out, arg_out = approx_max_k(operand, k, reduction_dimension,
                                    recall_target,
                                    reduction_input_size_override,
                                    aggregate_to_topk)
  else:
    val_out, arg_out = approx_min_k(operand, k, reduction_dimension,
                                    recall_target,
                                    reduction_input_size_override,
                                    aggregate_to_topk)
  if type(tangent) is ad_util.Zero:
    tangent_out = ad_util.p2tz(val_out)
  else:
    arg_shape = arg_out.shape
    rank = len(arg_shape)
    if reduction_dimension < 0:
      reduction_dimension += rank
    tangent_out = take_along_axis(tangent, arg_out, axis=reduction_dimension)
  return (val_out, arg_out), (tangent_out, ad_util.p2tz(arg_out))

