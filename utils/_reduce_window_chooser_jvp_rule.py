
def _reduce_window_chooser_jvp_rule(prim, g, operand, *, window_dimensions,
                                    window_strides, padding, base_dilation,
                                    window_dilation):
  assert prim is lax.max_p or prim is lax.min_p
  select_prim = lax.ge_p if prim is lax.max_p else lax.le_p
  return _select_and_gather_add(g, operand, select_prim, window_dimensions,
                                window_strides, padding, base_dilation,
                                window_dilation)

