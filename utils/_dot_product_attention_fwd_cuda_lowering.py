
def _dot_product_attention_fwd_cuda_lowering(
    ctx, query, key, value, bias, q_seqlen, kv_seqlen, q_offsets,
    kv_offsets, page_table_k, page_table_v, scale, seed, dropout_rate,
    variadic_args, mask_type, layout, sliding_window_length, is_training):
  query_type = ir.RankedTensorType(query.type)
  query_shape = query_type.shape
  value_type = ir.RankedTensorType(value.type)
  value_shape = value_type.shape

  if layout == AttentionLayout.BNTH.value:
    B, N, T, qk_H = query_shape
    _, _, S, v_H = value_shape
    output_layout = (3, 2, 1, 0)
    output_transpose_perm = mlir.dense_int_array((0, 1, 2, 3))
  else:
    B, T, N, qk_H = query_shape
    _, S, _, v_H = value_shape
    output_layout = (3, 1, 2, 0)
    output_transpose_perm = mlir.dense_int_array((0, 2, 1, 3))

  max_seg_per_batch = get_max_seg_per_batch(ir.RankedTensorType(q_offsets.type))
  is_paged_attention = check_is_paged_attention(ir.RankedTensorType(page_table_k.type))

  output_shape = (B, N, T, v_H)
  softmax_stat_shape = (B * max_seg_per_batch, N, T)
  workspace_shape = (0,)
  workspace_type = ir.IntegerType.get_unsigned(8)

  has_bias, _ = variadic_args
  backend_config = create_dot_product_attention_backend_config(
      B, N, T, S, query_type.element_type, scale, seed, dropout_rate,
      mask_type, layout, sliding_window_length, max_seg_per_batch,
      is_paged_attention, is_bwd=False)
  # {Q, K, V, bias*, q_seqlen*, kv_seqlen*,  q_offsets*, kv_offsets*}}
  # {output, activation*, workspace}
  has_dropout = dropout_rate > 0
  operands = [query, key, value]
  if has_bias:
    operands.append(bias)
  if has_padding(mask_type) or max_seg_per_batch > 1 or is_paged_attention:
    operands.append(q_seqlen)
    operands.append(kv_seqlen)
  if max_seg_per_batch > 1:
    operands.append(q_offsets)
    operands.append(kv_offsets)
  if is_paged_attention:
    operands.append(page_table_k)
    operands.append(page_table_v)

  custom_call_name = get_custom_call_name(has_bias, has_dropout, False)

  if is_training:
    result_types = [
      ir.RankedTensorType.get(output_shape, query_type.element_type),
      ir.RankedTensorType.get(softmax_stat_shape, ir.F32Type.get()),
      ir.RankedTensorType.get(workspace_shape, workspace_type),
    ]
    result_layouts = [output_layout] + default_layouts(softmax_stat_shape, workspace_shape)
  else:
    result_types = [
      ir.RankedTensorType.get(output_shape, query_type.element_type),
      ir.RankedTensorType.get(workspace_shape, workspace_type)
    ]
    result_layouts = [output_layout] + default_layouts(workspace_shape)
  # create custom call here
  out = mlir.custom_call(
    custom_call_name,
    result_types=result_types,
    operands=operands,
    backend_config=backend_config,
    operand_layouts=default_layouts(
      *[ir.RankedTensorType(operand.type).shape for operand in operands]),
    result_layouts=result_layouts,
  )
  # drop workspace memory
  # output should be (B, T, N, H) instead of (B, N, T, H)
  if is_training:
    return [hlo.transpose(out.results[0], output_transpose_perm), out.results[1]]
  else:
    return [hlo.transpose(out.results[0], output_transpose_perm)]

