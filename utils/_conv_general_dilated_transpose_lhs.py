
def _conv_general_dilated_transpose_lhs(
    g, lhs, rhs, *, window_strides, padding, lhs_dilation, rhs_dilation,
    dimension_numbers, feature_group_count, batch_group_count,
    precision, preferred_element_type, out_sharding):
  assert type(dimension_numbers) is ConvDimensionNumbers
  assert batch_group_count == 1 or feature_group_count == 1
  rhs_shape = rhs.shape
  lhs_shape = lhs.aval.shape
  lhs_sdims, rhs_sdims, out_sdims = map(_conv_sdims, dimension_numbers)
  lhs_spec, rhs_spec, out_spec = dimension_numbers
  t_rhs_spec = _conv_spec_transpose(rhs_spec)
  if feature_group_count > 1:
    # in addition to switching the dims in the spec, need to move the feature
    # group axis into the transposed rhs's output feature dim
    rhs = _reshape_axis_out_of(rhs_spec[0], feature_group_count, rhs)
    rhs = _reshape_axis_into(rhs_spec[0], rhs_spec[1], rhs)
  elif batch_group_count > 1:
    rhs = _reshape_axis_out_of(rhs_spec[0], batch_group_count, rhs)
    rhs = _reshape_axis_into(rhs_spec[0], rhs_spec[1], rhs)
    feature_group_count = batch_group_count
  trans_dimension_numbers = ConvDimensionNumbers(out_spec, t_rhs_spec, lhs_spec)
  padding = _conv_general_vjp_lhs_padding(
      np.take(lhs_shape, lhs_sdims), np.take(rhs_shape, rhs_sdims),
      window_strides, np.take(g.shape, out_sdims), padding, lhs_dilation,
      rhs_dilation)
  revd_weights = lax.rev(rhs, rhs_sdims)
  if g.dtype != revd_weights.dtype:
    revd_weights = lax.convert_element_type(revd_weights, g.dtype)
  out = conv_general_dilated(
      g, revd_weights, window_strides=lhs_dilation, padding=padding,
      lhs_dilation=window_strides, rhs_dilation=rhs_dilation,
      dimension_numbers=trans_dimension_numbers,
      feature_group_count=feature_group_count,
      batch_group_count=1, precision=precision,
      preferred_element_type=preferred_element_type,
      out_sharding=lhs.aval.sharding)
  if out.dtype != lhs.aval.dtype:
    out = lax.convert_element_type(out, lhs.aval.dtype)
  if batch_group_count > 1:
    out = _reshape_axis_out_of(lhs_spec[1], batch_group_count, out)
    out = _reshape_axis_into(lhs_spec[1], lhs_spec[0], out)
  return out

