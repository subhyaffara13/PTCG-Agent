
def _scaled_matmul_rocm_lowering(
    ctx, a, b, a_scales, b_scales, preferred_element_type
  ):
  # Lower `scaled_matmul` to `lax.scaled_dot` on ROCm so the backend can match
  # the `xla.scaled_dot` composite while preserving `scaled_matmul` semantics.
  def _scaled_dot_lowering_impl(lhs, rhs, lhs_scales, rhs_scales):
    return lax_internal.scaled_dot(
        lhs,
        rhs,
        lhs_scale=lhs_scales,
        rhs_scale=rhs_scales,
        #  `scaled_matmul` is canonicalized to (B, M, K) x (B, N, K), so we
        # contract over K (axis 2) and batch over B (axis 0), yielding (B, M, N).
        dimension_numbers=(((2,), (2,)), ((0,), (0,))),
        preferred_element_type=preferred_element_type,
    )
  return mlir.lower_fun(_scaled_dot_lowering_impl, multiple_results=False)(
      ctx, a, b, a_scales, b_scales
  )

