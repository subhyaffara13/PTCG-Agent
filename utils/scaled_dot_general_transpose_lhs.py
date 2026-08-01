
def scaled_dot_general_transpose_lhs(
    g, x, y, *, dimension_numbers, preferred_element_type, configs,
    swap_ans=False
  ):
  (x_contract, y_contract), (x_batch, y_batch) = dimension_numbers
  x_ndim = x.aval.ndim
  x_kept = remaining(range(x_ndim), x_contract, x_batch)
  y_kept = remaining(range(np.ndim(y)), y_contract, y_batch)
  if swap_ans:
    ans_batch, ans_y, _ = ranges_like(x_batch, y_kept, x_kept)
  else:
    ans_batch, _, ans_y = ranges_like(x_batch, x_kept, y_kept)

  x_contract_sorted_by_y = list(np.take(x_contract, np.argsort(y_contract)))
  out_axes = np.argsort(list(x_batch) + x_kept + x_contract_sorted_by_y)

  y_dn = (y_kept, y_batch)
  g_dn = (ans_y, ans_batch)

  y_3d = shape_normalization(y, y_dn)
  g_3d = shape_normalization(g, g_dn)

  g_config, y_config = configs[0], configs[1]
  if configs[0].mode != 'nvfp4':
    g_q, g_scales = quantize(g_3d, g_config)
    y_q, y_scales = quantize(y_3d, y_config)

    out = scaled_matmul_wrapper(
        g_q, y_q, g_scales, y_scales, preferred_element_type
    )
  else:
    out = jnp.matmul(g_3d, jnp.permute_dims(y_3d, (0, 2, 1)), preferred_element_type=preferred_element_type)

  expanded_out_shape = compute_dot_output_shape(g.shape, y.shape, g_dn, y_dn)
  expanded_out = jnp.reshape(out, expanded_out_shape)
  x_bar = lax.transpose(expanded_out, tuple(out_axes))
  return x_bar

