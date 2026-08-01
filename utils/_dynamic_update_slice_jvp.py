
def _dynamic_update_slice_jvp(primals, tangents):
  operand, update = primals[:2]
  start_indices = primals[2:]
  g_operand, g_update = tangents[:2]
  val_out = dynamic_update_slice_p.bind(operand, update, *start_indices)
  if type(g_operand) is ad_util.Zero and type(g_update) is ad_util.Zero:
    tangent_out = ad_util.p2tz(val_out)
  else:
    g_operand = ad.instantiate_zeros(g_operand)
    g_update = ad.instantiate_zeros(g_update)
    tangent_out = dynamic_update_slice_p.bind(g_operand, g_update, *start_indices)
  return val_out, tangent_out

