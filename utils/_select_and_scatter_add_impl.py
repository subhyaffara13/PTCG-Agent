
def _select_and_scatter_add_impl(source, operand, *,
                                 select_prim, window_dimensions, window_strides,
                                 padding, expand_padding):
  dtype = source.dtype
  select = lambda x, y: select_prim.bind(x, y)
  scatter = lax.bitwise_or if dtype == np.bool_ else lax.add
  original_padding = padding
  operand_shape = operand.shape
  if expand_padding:
    identity = (lax._get_max_identity if select_prim is lax.ge_p
                else lax._get_min_identity)
    pads = [(lo, hi, 0) for (lo, hi) in padding]
    operand = lax.pad(operand, identity(dtype), pads)
    padding = [(0, 0) for _ in padding]
  out = _select_and_scatter(
      operand, select, window_dimensions, window_strides, padding, source,
      lax._zero(operand), scatter)
  if expand_padding:
    start_indices = [lo for (lo, hi) in original_padding]
    stop_indices = [lo + d for ((lo, hi), d) in zip(original_padding,
                                                    operand_shape)]
    out = slicing.slice(out, start_indices, stop_indices)
  return out

