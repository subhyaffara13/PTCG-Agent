
def _conv_general_dilated_shape_rule(
    lhs: core.ShapedArray, rhs: core.ShapedArray, *, window_strides, padding,
    lhs_dilation, rhs_dilation, dimension_numbers, feature_group_count,
    batch_group_count, **unused_kwargs) -> tuple[int, ...]:
  assert type(dimension_numbers) is ConvDimensionNumbers
  if len(lhs.shape) != len(rhs.shape):
    msg = ("conv_general_dilated lhs and rhs must have the same number of "
           "dimensions, but got {} and {}.")
    raise ValueError(msg.format(lhs.shape, rhs.shape))
  if not feature_group_count > 0:
    msg = ("conv_general_dilated feature_group_count "
           "must be a positive integer, got {}.")
    raise ValueError(msg.format(feature_group_count))
  lhs_feature_count = lhs.shape[dimension_numbers.lhs_spec[1]]
  quot, rem = divmod(lhs_feature_count, feature_group_count)
  if rem:
    msg = ("conv_general_dilated feature_group_count must divide lhs feature "
           "dimension size, but {} does not divide {}.")
    raise ValueError(msg.format(feature_group_count, lhs_feature_count))
  if not core.definitely_equal(quot, rhs.shape[dimension_numbers.rhs_spec[1]]):
    msg = ("conv_general_dilated lhs feature dimension size divided by "
           "feature_group_count must equal the rhs input feature dimension "
           "size, but {} // {} != {}.")
    raise ValueError(msg.format(lhs_feature_count, feature_group_count,
                                rhs.shape[dimension_numbers.rhs_spec[1]]))
  if rhs.shape[dimension_numbers.rhs_spec[0]] % feature_group_count:
    msg = ("conv_general_dilated rhs output feature dimension size must be a "
           "multiple of feature_group_count, but {} is not a multiple of {}.")
    raise ValueError(msg.format(rhs.shape[dimension_numbers.rhs_spec[0]],
                                feature_group_count))

  if not batch_group_count > 0:
    msg = ("conv_general_dilated batch_group_count "
           "must be a positive integer, got {}.")
    raise ValueError(msg.format(batch_group_count))
  lhs_batch_count = lhs.shape[dimension_numbers.lhs_spec[0]]
  if batch_group_count > 1 and lhs_batch_count % batch_group_count != 0:
    msg = ("conv_general_dilated batch_group_count must divide lhs batch "
           "dimension size, but {} does not divide {}.")
    raise ValueError(msg.format(batch_group_count, lhs_batch_count))

  if rhs.shape[dimension_numbers.rhs_spec[0]] % batch_group_count:
    msg = ("conv_general_dilated rhs output feature dimension size must be a "
           "multiple of batch_group_count, but {} is not a multiple of {}.")
    raise ValueError(msg.format(rhs.shape[dimension_numbers.rhs_spec[0]],
                                batch_group_count))

  if batch_group_count > 1 and feature_group_count > 1:
    msg = ("At most one of batch_group_count and feature_group_count may be > "
           "1, got batch_group_count={} and feature_group_count={}")
    raise ValueError(msg.format(batch_group_count, feature_group_count))

  if len(_conv_sdims(dimension_numbers.rhs_spec)) != len(window_strides):
    msg = ("conv_general_dilated window and window_strides must have "
           "the same number of dimensions, but got {} and {}")
    raise ValueError(
        msg.format(len(_conv_sdims(dimension_numbers.rhs_spec)), len(window_strides)))

  lhs_perm, rhs_perm, out_perm = dimension_numbers
  lhs_trans = lax._dilate_shape(np.take(lhs.shape, lhs_perm), lhs_dilation)
  rhs_trans = lax._dilate_shape(np.take(rhs.shape, rhs_perm), rhs_dilation)
  out_trans = conv_shape_tuple(lhs_trans, rhs_trans, window_strides, padding,
                               batch_group_count)
  return tuple(np.take(out_trans, np.argsort(out_perm)))

