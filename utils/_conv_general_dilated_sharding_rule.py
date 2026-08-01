
def _conv_general_dilated_sharding_rule(
    lhs: core.ShapedArray, rhs: core.ShapedArray, *, window_strides, padding,
    lhs_dilation, rhs_dilation, dimension_numbers, feature_group_count,
    batch_group_count, out_sharding, **unused_kwargs):
  if out_sharding is not None:
    assert isinstance(out_sharding, NamedSharding)
    return out_sharding
  # Only allow if rhs is fully replicated and lhs's feature dim is not sharded
  if ((rhs.sharding.mesh.empty or rhs.sharding.is_fully_replicated) and
      lhs.sharding.spec[dimension_numbers.lhs_spec[1]] is None):
    out_shape = _conv_general_dilated_shape_rule(
        lhs, rhs, window_strides=window_strides, padding=padding,
        lhs_dilation=lhs_dilation, rhs_dilation=rhs_dilation,
        dimension_numbers=dimension_numbers,
        feature_group_count=feature_group_count,
        batch_group_count=batch_group_count)
    return lax.slicing._get_sharding_for_varying_out_shape(
        out_shape, lhs, "conv_general_dilated")
  raise core.ShardingTypeError(
      "Please specify the output sharding via `out_sharding` parameter of"
      " `conv_general_dilated`")

