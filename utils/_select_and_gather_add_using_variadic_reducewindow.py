
def _select_and_gather_add_using_variadic_reducewindow(
    tangents, operand, *, select_prim, window_dimensions, window_strides,
    padding, base_dilation, window_dilation):
  def reducer(x, y):
    kx, vx = x
    ky, vy = y
    which = select_prim.bind(kx, ky)
    return (lax.select(which, kx, ky), lax.select(which, vx, vy))

  assert select_prim is lax.ge_p or select_prim is lax.le_p, select_prim
  init = -np.inf if select_prim is lax.ge_p else np.inf
  _, out = reduce_window(
    (operand, tangents),
    (np.array(init, dtype=operand.dtype), np.array(0, dtype=operand.dtype)),
    reducer, window_dimensions, window_strides, padding, base_dilation,
    window_dilation)
  return out

