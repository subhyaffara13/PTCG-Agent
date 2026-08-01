
def _dot_product_attention_fp8_fwd_cuda_lowering(
    ctx, query, key, value,
    descale_q, descale_k, descale_v, descale_s, scale_s, scale_o,
    scale, use_causal_mask, layout, is_training):
  query_type = ir.RankedTensorType(query.type)
  query_shape = query_type.shape
  key_type = ir.RankedTensorType(key.type)
  key_shape = key_type.shape

  if layout == AttentionLayout.BNTH.value:
    B, N, T, H = query_shape
    _, _, S, _ = key_shape
    output_layout = (3, 2, 1, 0)
    output_transpose_perm = mlir.dense_int_array((0, 1, 2, 3))
  else:
    B, T, N, H = query_shape
    _, S, _, _ = key_shape
    output_layout = (3, 1, 2, 0)
    output_transpose_perm = mlir.dense_int_array((0, 2, 1, 3))

  output_shape = (B, N, T, H)
  softmax_stat_shape = (B, N, T)
  workspace_shape = (0,)
  amax_shape = (1,1,1,1)
  workspace_type = ir.IntegerType.get_unsigned(8)
  mask_type = MaskType.CAUSAL if use_causal_mask else MaskType.NO_MASK
  backend_config = create_dot_product_attention_fp8_backend_config(
      B, N, T, S, ir.BF16Type.get(),  # query_type.element_type,
      scale, mask_type, layout, is_bwd=False,
  )

  operands = [query, key, value, descale_q, descale_k, descale_v, descale_s, scale_s, scale_o]
  custom_call_name = get_fp8_custom_call_name(is_bwd=False)

  if is_training:
    result_types = [
      ir.RankedTensorType.get(output_shape, query_type.element_type),
      ir.RankedTensorType.get((1,1,1,1), ir.F32Type.get()),
      ir.RankedTensorType.get((1,1,1,1), ir.F32Type.get()),
      ir.RankedTensorType.get(softmax_stat_shape, ir.F32Type.get()),
      ir.RankedTensorType.get(workspace_shape, workspace_type),
    ]
    result_layouts = [output_layout] + default_layouts(amax_shape, amax_shape, softmax_stat_shape, workspace_shape)
  else:
    result_types = [
      ir.RankedTensorType.get(output_shape, query_type.element_type),
      ir.RankedTensorType.get((1,1,1,1), ir.F32Type.get()),
      ir.RankedTensorType.get((1,1,1,1), ir.F32Type.get()),
      ir.RankedTensorType.get(workspace_shape, workspace_type)
    ]
    result_layouts = [output_layout] + default_layouts(amax_shape, amax_shape, workspace_shape)

  operand_shapes = [ir.RankedTensorType(operand.type).shape for operand in operands[:3]]
  operand_shapes += [[1, 1, 1, 1]] * 6
  operand_layouts = default_layouts(*operand_shapes)
  out = mlir.custom_call(
    custom_call_name,
    result_types=result_types,
    operands=operands,
    backend_config=backend_config,
    operand_layouts=operand_layouts,
    result_layouts=result_layouts,
  )

  if is_training:
    return [hlo.transpose(out.results[0], output_transpose_perm), out.results[1], out.results[2], out.results[3]]
  else:
    return [hlo.transpose(out.results[0], output_transpose_perm), out.results[1], out.results[2]]

