
def _vector_shape_cast_op_lowering_rule(
    _: LoweringContext, op: vector.ShapeCastOp
) -> Sequence[ir.Value]:
  [layout] = inference_utils.in_layouts(op)
  out_vec_ty = ir.VectorType(op.result.type)
  assert out_vec_ty.has_static_shape
  a = _fragmented_array_from_ir(op.source, layout)
  return [
      fragmented_array_to_ir(a.reshape(tuple(out_vec_ty.shape)), out_vec_ty)
  ]

