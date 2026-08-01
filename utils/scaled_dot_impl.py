
def scaled_dot_impl(lhs, rhs, dimension_numbers, preferred_element_type,
                    configs):
  if preferred_element_type is None:
    preferred_element_type = dtypes.result_type(
        lhs, rhs, return_weak_type_flag=False
    )
  else:
    preferred_element_type = dtypes.check_and_canonicalize_user_dtype(
        preferred_element_type, "scaled_dot_impl")

  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  lhs_dn = (lhs_contract, lhs_batch)
  rhs_dn = (rhs_contract, rhs_batch)

  lhs_3d = shape_normalization(lhs, lhs_dn)
  rhs_3d = shape_normalization(rhs, rhs_dn)
  lhs_config, rhs_config = configs[0], configs[1]
  lhs_q, lhs_scales = quantize(lhs_3d, lhs_config)
  rhs_q, rhs_scales = quantize(rhs_3d, rhs_config)

  out_dtype = preferred_element_type
  if configs[0].mode == 'nvfp4':
    out_dtype = np.float32

  out = scaled_matmul_wrapper(
      lhs_q, rhs_q, lhs_scales, rhs_scales, preferred_element_type=out_dtype
  )

  if configs[0].mode == 'nvfp4':
    out *= (configs[0].global_scale * configs[1].global_scale)
    out = out.astype(preferred_element_type)

  expanded_out_shape = compute_dot_output_shape(
      lhs.shape, rhs.shape, lhs_dn, rhs_dn
  )
  expanded_out = jnp.reshape(out, expanded_out_shape)
  return expanded_out

