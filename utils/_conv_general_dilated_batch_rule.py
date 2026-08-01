
def _conv_general_dilated_batch_rule(
    axis_data,
    batched_args,
    batch_dims,
    *, window_strides, padding,
    lhs_dilation, rhs_dilation, dimension_numbers,
    feature_group_count, batch_group_count, precision,
    preferred_element_type, out_sharding, **unused_kwargs):
  lhs, rhs = batched_args
  lhs_bdim, rhs_bdim = batch_dims
  lhs_spec, rhs_spec, out_spec = dimension_numbers
  if lhs_bdim is None and rhs_bdim is None:
    out = conv_general_dilated_p.bind(
        lhs, rhs, window_strides=window_strides, padding=padding,
        lhs_dilation=lhs_dilation, rhs_dilation=rhs_dilation,
        dimension_numbers=dimension_numbers,
        feature_group_count=feature_group_count,
        batch_group_count=batch_group_count, precision=precision,
        preferred_element_type=preferred_element_type,
        out_sharding=out_sharding, **unused_kwargs)
    return out, None

  assert batch_group_count == 1 or feature_group_count == 1

  # Some of the cases that reshape into batch or feature dimensions do not work
  # with size 0 batch dimensions. The best fix would be to extend HLO to support
  # multiple batch dimensions.
  if ((lhs_bdim is not None and lhs.shape[lhs_bdim] == 0) or
      (rhs_bdim is not None and rhs.shape[rhs_bdim] == 0)):
    lhs_shape_unbatched, rhs_shape_unbatched = list(lhs.shape), list(rhs.shape)
    if lhs_bdim is not None:
      lhs_shape_unbatched.pop(lhs_bdim)
    if rhs_bdim is not None:
      rhs_shape_unbatched.pop(rhs_bdim)
    shape = _conv_general_dilated_shape_rule(
      core.ShapedArray(lhs_shape_unbatched, lhs.dtype),
      core.ShapedArray(rhs_shape_unbatched, rhs.dtype),
      window_strides=window_strides, padding=padding, lhs_dilation=lhs_dilation,
      rhs_dilation=rhs_dilation, dimension_numbers=dimension_numbers,
      feature_group_count=feature_group_count,
      batch_group_count=batch_group_count)
    if out_sharding is not None:
      out_sharding = batching.get_sharding_for_vmap(axis_data, out_sharding, 0)
    return lax.full(
      (0,) + shape, 0,
      dtype=lhs.dtype if preferred_element_type is None
            else preferred_element_type,
            sharding=out_sharding), 0

  def get_out_sharding(axis):
    if out_sharding is None:
      return None
    val = axis_data.explicit_mesh_axis
    if not val:
      return out_sharding
    if out_sharding.spec[axis] is not None:
      # Batch dim must not already be sharded.
      raise NotImplementedError
    return NamedSharding(out_sharding.mesh,
                         P(*util.tuple_update(out_sharding.spec, axis, val)))

  if lhs_bdim is not None and rhs_bdim is not None:
    assert lhs.shape[lhs_bdim] == rhs.shape[rhs_bdim]
    if batch_group_count > 1:
      new_lhs = _reshape_axis_into(lhs_bdim, lhs_spec[0], lhs)
      batch_group_count *= lhs.shape[lhs_bdim]
    else:
      new_lhs = _reshape_axis_into(lhs_bdim, lhs_spec[1], lhs)
      feature_group_count *= lhs.shape[lhs_bdim]
    new_rhs = _reshape_axis_into(rhs_bdim, rhs_spec[0], rhs)
    out = conv_general_dilated(
      new_lhs, new_rhs, window_strides, padding, lhs_dilation, rhs_dilation,
      dimension_numbers, feature_group_count=feature_group_count,
      batch_group_count=batch_group_count, precision=precision,
      preferred_element_type=preferred_element_type,
      out_sharding=get_out_sharding(out_spec[1]))
    out = _reshape_axis_out_of(out_spec[1], lhs.shape[lhs_bdim], out)
    return out, out_spec[1]

  elif lhs_bdim is not None:
    if batch_group_count == 1:
      new_lhs = _reshape_axis_into(lhs_bdim, lhs_spec[0], lhs)
      out = conv_general_dilated(new_lhs, rhs, window_strides, padding,
                                 lhs_dilation, rhs_dilation, dimension_numbers,
                                 feature_group_count, precision=precision,
                                 preferred_element_type=preferred_element_type,
                                 out_sharding=get_out_sharding(out_spec[0]))
      out = _reshape_axis_out_of(out_spec[0], lhs.shape[lhs_bdim], out)
      return out, out_spec[0]
    else:
      new_lhs = _reshape_axis_out_of(lhs_spec[0] + int(lhs_bdim <= lhs_spec[0]),
                                     batch_group_count, lhs)
      new_lhs = _reshape_axis_into(lhs_bdim + int(lhs_spec[0] < lhs_bdim),
                                   lhs_spec[0] + 1,
                                   new_lhs)
      new_lhs = _reshape_axis_into(lhs_spec[0], lhs_spec[0], new_lhs)
      out = conv_general_dilated(new_lhs, rhs, window_strides, padding,
                                 lhs_dilation, rhs_dilation, dimension_numbers,
                                 feature_group_count, batch_group_count,
                                 precision=precision,
                                 preferred_element_type=preferred_element_type,
                                 out_sharding=get_out_sharding(out_spec[0]))
      out = _reshape_axis_out_of(out_spec[0], lhs.shape[lhs_bdim], out)
      return out, out_spec[0]

  elif rhs_bdim is not None:
    if feature_group_count == 1 and batch_group_count == 1:
      new_rhs = _reshape_axis_into(rhs_bdim, rhs_spec[0], rhs)
      out = conv_general_dilated(lhs, new_rhs, window_strides, padding,
                                 lhs_dilation, rhs_dilation, dimension_numbers,
                                 feature_group_count, batch_group_count,
                                 precision=precision,
                                 preferred_element_type=preferred_element_type,
                                 out_sharding=get_out_sharding(out_spec[1]))
      out = _reshape_axis_out_of(out_spec[1], rhs.shape[rhs_bdim], out)
      return out, out_spec[1]
    else:
      if out_sharding is not None:
        raise NotImplementedError
      # groups need to be outermost, so we need to factor them out of the
      # rhs output feature dim, then factor the batch dim into the remaining rhs
      # output feature dim, then put groups back in. We do something
      # similar on the output. An alternative which would require more FLOPs but
      # fewer reshapes would be to broadcast lhs.
      group_count = (feature_group_count if feature_group_count > 1
                     else batch_group_count)
      new_rhs = _reshape_axis_out_of(rhs_spec[0] + int(rhs_bdim <= rhs_spec[0]),
                                     group_count, rhs)
      new_rhs = _reshape_axis_into(rhs_bdim + int(rhs_spec[0] < rhs_bdim),
                                   rhs_spec[0] + 1, new_rhs)
      new_rhs = _reshape_axis_into(rhs_spec[0], rhs_spec[0], new_rhs)
      out = conv_general_dilated(lhs, new_rhs, window_strides, padding,
                                 lhs_dilation, rhs_dilation, dimension_numbers,
                                 feature_group_count, batch_group_count,
                                 precision=precision,
                                 preferred_element_type=preferred_element_type,
                                 out_sharding=get_out_sharding(out_spec[1]))
      out = _reshape_axis_out_of(out_spec[1], group_count, out)
      out = _reshape_axis_out_of(out_spec[1] + 1, rhs.shape[rhs_bdim], out)
      out = _reshape_axis_into(out_spec[1], out_spec[1] + 1, out)
      return out, out_spec[1]

