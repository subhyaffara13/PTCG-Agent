
def _dot_product_attention_bwd_cuda_lowering(
    ctx, query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
    page_table_k, page_table_v, activation, fwd_output, grad_output,
    scale, seed, dropout_rate, variadic_args, mask_type, layout, sliding_window_length):
  query_type = ir.RankedTensorType(query.type)
  query_shape = query_type.shape
  key_type = ir.RankedTensorType(key.type)
  value_type = ir.RankedTensorType(value.type)
  value_shape = value_type.shape

  if layout == AttentionLayout.BNTH.value:
    B, q_N, T, qk_H = query_shape
    _, v_N, S, v_H = value_shape
    grad_layout = (3, 2, 1, 0)
    grad_transpose_perm = mlir.dense_int_array((0, 1, 2, 3))
  else:
    B, T, q_N, qk_H = query_shape
    _, S, v_N, v_H = value_shape
    grad_layout = (3, 1, 2, 0)
    grad_transpose_perm = mlir.dense_int_array((0, 2, 1, 3))

  workspace_shape = (0,)
  workspace_type = ir.IntegerType.get_unsigned(8)

  grad_query_shape = (B, q_N, T, qk_H)
  grad_key_shape = (B, v_N, S, qk_H)
  grad_value_shape = (B, v_N, S, v_H)

  has_bias, has_dbias = variadic_args
  max_seg_per_batch = get_max_seg_per_batch(ir.RankedTensorType(q_offsets.type))
  backend_config = create_dot_product_attention_backend_config(
      B, q_N, T, S, query_type.element_type, scale, seed, dropout_rate,
      mask_type, layout, sliding_window_length, max_seg_per_batch,
      False, is_bwd=True)
  # {Q, K, V, activation, dO, bias*, O, q_seqlen*, kv_seqlen*,
  #  q_offsets*, kv_offsets*}
  # {dQ, dK, dV, dbias*, workspace}
  has_dropout = dropout_rate > 0
  # create operands
  operands = [query, key, value, activation, grad_output]
  if has_bias:
    # flash attention requires bias in the bwd for remat
    operands.append(bias)
  operands.append(fwd_output)
  if has_padding(mask_type) or max_seg_per_batch > 1:
    operands.append(q_seqlen)
    operands.append(kv_seqlen)
  if max_seg_per_batch > 1:
    operands.append(q_offsets)
    operands.append(kv_offsets)
  # get custom call name
  custom_call_name = get_custom_call_name(has_bias, has_dropout, True)

  # create output types and layouts
  # grad_query, grad_key, grad_value
  result_types = [
    ir.RankedTensorType.get(grad_query_shape, query_type.element_type),
    ir.RankedTensorType.get(grad_key_shape, key_type.element_type),
    ir.RankedTensorType.get(grad_value_shape, value_type.element_type),
  ]
  result_layouts = [grad_layout, grad_layout, grad_layout]
  bias_type = ir.RankedTensorType(bias.type)
  bias_shape = bias_type.shape
  if has_dbias:
    # cuDNN supports bias for this case
    result_types.append(
      ir.RankedTensorType.get(bias_shape, bias_type.element_type))
    result_layouts = result_layouts + default_layouts(bias_shape)
  # workspace
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
  dqkv = (hlo.transpose(out.results[0], grad_transpose_perm),
          hlo.transpose(out.results[1], grad_transpose_perm),
          hlo.transpose(out.results[2], grad_transpose_perm))
  # Only keep dQ, dK, dV and dBias here
  if has_dbias:
    return dqkv + (out.results[3],)
  else:
    return dqkv

