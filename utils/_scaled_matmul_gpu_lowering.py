import json

def _scaled_matmul_gpu_lowering(
    ctx, a, b, a_scales, b_scales, preferred_element_type
  ):
  lhs_type = ir.RankedTensorType(a.type)
  lhs_shape = lhs_type.shape
  rhs_type = ir.RankedTensorType(b.type)
  rhs_shape = rhs_type.shape

  batch, non_contracting_lhs, contracting = lhs_shape
  _, non_contracting_rhs, _ = rhs_shape
  result_shape = (batch, non_contracting_lhs, non_contracting_rhs)

  out_type = mlir.dtype_to_ir_type(preferred_element_type)
  result_types = [ir.RankedTensorType.get(result_shape, out_type)]

  operands = [a, b, a_scales, b_scales]
  backend_config = {
      "scaled_dot_backend_config": {
          "lhs_batch_dimensions": [0],
          "rhs_batch_dimensions": [0],
          "dequantize_type": element_type_to_backend_config_type(out_type),
      }
  }

  backend_config = json.dumps(backend_config)
  out = mlir.custom_call(
      block_scaled_dot_name,
      result_types=result_types,
      operands=operands,
      backend_config=backend_config,
      operand_layouts=default_layouts(
          *[ir.RankedTensorType(operand.type).shape for operand in operands]
      ),
      result_layouts=default_layouts(result_shape),
  )
  return [out.result]

