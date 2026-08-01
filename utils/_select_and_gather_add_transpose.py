
def _select_and_gather_add_transpose(
    t, tangents, operand, *, select_prim, window_dimensions, window_strides,
    padding, base_dilation, window_dilation):
  assert select_prim in (lax.le_p, lax.ge_p)
  assert (ad.is_undefined_primal(tangents) and
          not ad.is_undefined_primal(operand))
  if any(d != 1 for d in window_dilation):
    msg = ("VJP not implemented for select_and_gather (MaxPool) with window "
           "dilation, got window_dilation={}.")
    raise NotImplementedError(msg.format(window_dilation))
  if type(t) is ad_util.Zero:
    return [ad_util.Zero(tangents.aval), None]
  has_base_dilation = any(d != 1 for d in base_dilation)
  if has_base_dilation:
    select_identity = (lax._get_max_identity if select_prim is lax.ge_p
                       else lax._get_min_identity)
    operand = lax.pad(operand, select_identity(operand.dtype),
                      tuple((0, 0, d - 1) for d in base_dilation))
  result = _select_and_scatter_add(t, operand, select_prim, window_dimensions,
                                   window_strides, padding)
  if has_base_dilation:
    result = slicing.slice(result, (0,) * len(result.shape), result.shape,
                           base_dilation)
  return [result, None]

