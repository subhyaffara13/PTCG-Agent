
def _select_and_gather_add_jvp(
    primals, tangents, *, select_prim, window_dimensions, window_strides,
    padding, base_dilation, window_dilation):
  source, operand = primals
  g_source, g_operand = tangents
  val_out = _select_and_gather_add(
      source, operand, select_prim, window_dimensions, window_strides,
      padding, base_dilation, window_dilation)
  del g_operand
  if type(g_source) is ad_util.Zero:
    tangent_out = ad_util.p2tz(val_out)
  else:
    tangent_out = _select_and_gather_add(
        g_source, operand, select_prim, window_dimensions,
        window_strides, padding, base_dilation, window_dilation)
  return val_out, tangent_out

