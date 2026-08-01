
def _dot_product_attention_fp8_bwd_cuda_lowering(
    ctx, query, key, value, fwd_output, grad_output, activation,
    descale_q, descale_k, descale_v, descale_o, descale_dO, descale_s,
    descale_dP, scale_s, scale_dQ, scale_dK, scale_dV, scale_dP, scale,
    use_causal_mask, layout):
  query_type = ir.RankedTensorType(query.type)
  query_shape = query_type.shape
  key_type = ir.RankedTensorType(key.type)
  key_shape = key_type.shape
  value_type = ir.RankedTensorType(value.type)

  if layout == AttentionLayout.BNTH.value:
    B, q_N, T, H = query_shape
    _, k_N, S, _ = key_shape
    grad_layout = (3, 2, 1, 0)
    grad_transpose_perm = mlir.dense_int_array((0, 1, 2, 3))
  else:
    B, T, q_N, H = query_shape
    _, S, k_N, _ = key_shape
    grad_layout = (3, 1, 2, 0)
    grad_transpose_perm = mlir.dense_int_array((0, 2, 1, 3))

  workspace_shape = (0,)
  workspace_type = ir.IntegerType.get_unsigned(8)
  amax_shape = (1,1,1,1)

  grad_query_shape = (B, q_N, T, H)
  grad_key_shape = (B, k_N, S, H)
  grad_value_shape = (B, k_N, S, H)
  mask_type = MaskType.CAUSAL if use_causal_mask else MaskType.NO_MASK

  backend_config = create_dot_product_attention_fp8_backend_config(
      B, q_N, T, S, ir.BF16Type.get(),
      scale, mask_type, layout, is_bwd=True,
  )

  operands = [
    query,
    key,
    value,
    fwd_output,
    grad_output,
    activation,
    descale_q,
    descale_k,
    descale_v,
    descale_o,
    descale_dO,
    descale_s,
    descale_dP,
    scale_s,
    scale_dQ,
    scale_dK,
    scale_dV,
    scale_dP,
  ]

  custom_call_name = get_fp8_custom_call_name(is_bwd=True)

  result_types = [
    ir.RankedTensorType.get(grad_query_shape, query_type.element_type),
    ir.RankedTensorType.get(grad_key_shape, key_type.element_type),
    ir.RankedTensorType.get(grad_value_shape, value_type.element_type),
    ir.RankedTensorType.get(amax_shape, ir.F32Type.get()),
    ir.RankedTensorType.get(amax_shape, ir.F32Type.get()),
    ir.RankedTensorType.get(amax_shape, ir.F32Type.get()),
    ir.RankedTensorType.get(amax_shape, ir.F32Type.get()),
  ]
  result_layouts = [grad_layout, grad_layout, grad_layout] + default_layouts(amax_shape, amax_shape, amax_shape, amax_shape)

  result_types.append(ir.RankedTensorType.get(workspace_shape, workspace_type))
  result_layouts = result_layouts + default_layouts(workspace_shape)
  out = mlir.custom_call(
    custom_call_name,
    result_types=result_types,
    operands=operands,
    backend_config=backend_config,
    operand_layouts=default_layouts(
      *[ir.RankedTensorType(operand.type).shape for operand in operands]),
    result_layouts=result_layouts,
  )
  dqkv_amaxs = (hlo.transpose(out.results[0], grad_transpose_perm),
          hlo.transpose(out.results[1], grad_transpose_perm),
          hlo.transpose(out.results[2], grad_transpose_perm),
          out.results[3], out.results[4], out.results[5], out.results[6])
  # Only keep dQ, dK, dV, amax_dQ, amax_dK, amax_dV, amax_dP here
  return dqkv_amaxs

