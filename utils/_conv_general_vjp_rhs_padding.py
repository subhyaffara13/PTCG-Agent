
def _conv_general_vjp_rhs_padding(
    in_shape, window_dimensions, window_strides, out_shape, padding,
    lhs_dilation, rhs_dilation):

  if len(in_shape) == 0:  # 0D conv
    return []
  lhs_dilated_shape = lax._dilate_shape(in_shape, lhs_dilation)
  rhs_dilated_shape = lax._dilate_shape(window_dimensions, rhs_dilation)
  out_dilated_shape = lax._dilate_shape(out_shape, window_strides)
  pads_lo, _ = util.unzip2(padding)
  pads_from_lhs = map(operator.sub, out_dilated_shape, lhs_dilated_shape)
  pads_from_rhs = tuple(rd - pd - 1 for rd, pd in zip(rhs_dilated_shape, pads_lo))
  pads_hi = tuple(map(operator.add, pads_from_lhs, pads_from_rhs))
  return list(zip(pads_lo, pads_hi))

