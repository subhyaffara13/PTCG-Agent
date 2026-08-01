
def _dot_product_attention_fp8_bwd_rule(
    scale, use_causal_mask, layout, cudnn_version, res, g):
  (query, key, value, activation, fwd_output, aux_params) = res
  grad_output = g[0]
  grads = _dot_product_attention_fp8_bwd_p_wrapper.bind(
    query,
    key,
    value,
    fwd_output,
    grad_output,
    activation,
    *aux_params,
    scale=scale,
    use_causal_mask=use_causal_mask,
    layout=layout,
    )

  fp8_params_grads = dict.fromkeys(fp8_params_keys)
  keys_to_grad_indices = ['amax_dQ', 'amax_dK', 'amax_dV', 'amax_dP']
  # grads structure: (dQ, dK, dV, amax_dq, amax_dk, amax_dv, amax_dp)
  for i, key in enumerate(keys_to_grad_indices, start=3):
    fp8_params_grads[key] = grads[i]

  return (grads[0], grads[1], grads[2], fp8_params_grads)

