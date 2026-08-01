
def _conv_general_vjp_lhs_padding(
    in_shape, window_dimensions, window_strides, out_shape, padding,
    lhs_dilation, rhs_dilation) -> list[tuple[int, int]]:
  lhs_dilated_shape = lax._dilate_shape(in_shape, lhs_dilation)
  rhs_dilated_shape = lax._dilate_shape(window_dimensions, rhs_dilation)
  out_dilated_shape = lax._dilate_shape(out_shape, window_strides)
  pad_before = np.subtract(rhs_dilated_shape, [lo for lo, _ in padding]) - 1
  pad_after = (np.add(lhs_dilated_shape, rhs_dilated_shape) - 1
               - out_dilated_shape - pad_before)
  return util.safe_zip(pad_before, pad_after)

