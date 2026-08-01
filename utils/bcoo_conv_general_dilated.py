
def bcoo_conv_general_dilated(lhs, rhs, *, window_strides, padding,
                              lhs_dilation=None, rhs_dilation=None, dimension_numbers=None,
                              feature_group_count=1, batch_group_count=1, precision=None,
                              preferred_element_type=None,
                              out_sharding=None) -> BCOO:
  # Validate and process parameters using lax.conv_general_dilated abstract evaluation.
  func = functools.partial(
      lax.conv_general_dilated,
      window_strides=window_strides, padding=padding,
      lhs_dilation=lhs_dilation, rhs_dilation=rhs_dilation, dimension_numbers=dimension_numbers,
      feature_group_count=feature_group_count, batch_group_count=batch_group_count,
      precision=precision, preferred_element_type=preferred_element_type,
      out_sharding=out_sharding)
  jaxpr = jax.make_jaxpr(func)(jax.ShapeDtypeStruct(lhs.shape, lhs.dtype),
                               jax.ShapeDtypeStruct(rhs.shape, rhs.dtype))
  assert isinstance(jaxpr, core.ClosedJaxpr) and len(jaxpr.eqns) == 1
  params = jaxpr.eqns[0].params

  if params['lhs_dilation'] !=  (1,) * (lhs.ndim - 2):
    raise NotImplementedError("bcoo convolution with lhs_dilation.")
  if params['rhs_dilation'] != (1,) * (rhs.ndim - 2):
    raise NotImplementedError("bcoo convolution with lhs_dilation.")
  if params['window_strides'] != (1,) * (lhs.ndim - 2):
    raise NotImplementedError("bcoo convolution with non-unit window_strides.")
  if params['batch_group_count'] != params['feature_group_count'] != 1:
    raise NotImplementedError("bcoo convolution with non-unit group counts.")

  if lhs.shape[:2] != rhs.shape[:2] != (1, 1):
    raise NotImplementedError("bcoo convolution with leading dimensions other than (1, 1)")

  index_dtype = (lhs.indices.dtype if hasattr(lhs, 'indices')
                 else rhs.indices.dtype if hasattr(rhs, 'indices')
                 else 'int32')

  padding, = params['padding']
  return _bcoo_conv_1d(_convert_to_1d_for_conv(lhs, index_dtype),
                       _convert_to_1d_for_conv(rhs, index_dtype),
                       padding=padding)

