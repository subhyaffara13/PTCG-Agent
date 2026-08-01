
def _select_and_scatter_add_jvp(
    primals, tangents, *, select_prim, window_dimensions, window_strides,
    padding):
  source, operand = primals
  g_source, g_operand = tangents
  val_out = _select_and_scatter_add(
      source, operand, select_prim, window_dimensions, window_strides,
      padding)
  del g_operand
  if type(g_source) is ad_util.Zero:
    tangent_out = ad_util.p2tz(val_out)
  else:
    tangent_out = _select_and_scatter_add(
        g_source, operand, select_prim, window_dimensions,
        window_strides, padding)
  return val_out, tangent_out

