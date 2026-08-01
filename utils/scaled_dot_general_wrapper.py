
def scaled_dot_general_wrapper(
    lhs, rhs, dimension_numbers,
    preferred_element_type=np.float32,
    configs: list[BlockScaleConfig] | None=None,
  ):
  if preferred_element_type not in (np.dtype('float32'), np.dtype('bfloat16'), np.dtype('float16')):
    msg = ('Only support preferred_element_type in (f32, bf16, f16), but got '
            '{preferred_element_type}')
    raise TypeError(msg)
  if configs is None:
    mxfp8_config = BlockScaleConfig(
        mode='mxfp8',
        block_size=32,
        data_type=dtypes.float8_e4m3fn,
        scale_type=dtypes.float8_e8m0fnu,
        global_scale=None,
        infer_only=False
    )
    configs = [mxfp8_config, mxfp8_config, mxfp8_config]

  dimension_numbers = ensure_tuple(dimension_numbers)
  lhs_batched, rhs_batched, dn_batched = _ensure_batch_dim(
      lhs, rhs, dimension_numbers
  )
  out = scaled_dot_general_fn(
      lhs_batched, rhs_batched, dn_batched, preferred_element_type, configs,
  )

  # Expanding batch dims for operands adds a singleton batch dim at axis 0 in
  # the output, which we need to squeeze.
  if dn_batched != dimension_numbers:
    return jnp.squeeze(out, axis=0)
  return out

