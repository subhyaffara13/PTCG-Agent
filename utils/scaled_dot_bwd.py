
def scaled_dot_bwd(dimension_numbers, preferred_element_type, configs, res, g):
  (lhs, rhs) = res

  args = [g, lhs, rhs]
  kw_args = {
      "dimension_numbers": dimension_numbers,
      "preferred_element_type": preferred_element_type,
  }
  lhs_kw_args = {
      **kw_args,
      "configs": [configs[2], configs[1]]
  }
  rhs_kw_args = {
      **kw_args,
      "configs": [configs[2], configs[0]]
  }
  grad_lhs = scaled_dot_general_transpose_lhs(*args, **lhs_kw_args)
  grad_rhs = scaled_dot_general_transpose_rhs(*args, **rhs_kw_args)

  # We apply a Straight-Through Estimator (STE) with zero-out behavior: if
  # inputs are clipped during quantization in fprop, their corresponding gradients
  # are zeroed out; otherwise, they pass through unchanged.
  if configs[2].mode == "nvfp4":
    assert rhs.dtype == lhs.dtype
    MAX = dtypes.finfo(configs[0].data_type).max.astype(lhs.dtype)
    SCALE_MAX = dtypes.finfo(configs[0].scale_type).max.astype(lhs.dtype)
    grad_lhs = jnp.where(jnp.abs(lhs) <= configs[0].global_scale * MAX * SCALE_MAX, grad_lhs, 0)
    grad_rhs = jnp.where(jnp.abs(rhs) <= configs[1].global_scale * MAX * SCALE_MAX, grad_rhs, 0)

  return (grad_lhs, grad_rhs)

