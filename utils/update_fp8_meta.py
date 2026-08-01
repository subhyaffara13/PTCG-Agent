
def update_fp8_meta(
  x, q_dtype, scale, amax_history
):
  is_fmax32 = (scale.dtype == fm32 and amax_history.dtype == fm32)
  # convert fm32->f32 so we can do math
  if is_fmax32:
    amax_history = lax.convert_element_type(amax_history, jnp.float32)
    scale = lax.convert_element_type(scale, jnp.float32)

  # Update the fp8 meta
  dtype_max = get_fp8_max(q_dtype, jnp.float32)
  amax_from_history = jnp.max(amax_history, axis=0)

  new_scale = compute_scale(amax_from_history, scale, dtype_max)
  new_history = compute_amax_history(x, amax_history)

  if is_fmax32:
    new_history = lax.convert_element_type(new_history, fp32_max_grad)
    new_scale = lax.convert_element_type(new_scale, fp32_max_grad)
  return new_scale, new_history

