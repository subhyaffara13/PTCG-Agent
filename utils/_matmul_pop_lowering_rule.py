
def _matmul_pop_lowering_rule(
    ctx: LoweringRuleContext,
    *,
    acc_addr: int,
    mxu_index: int,
    shape: tuple[int, int],
    dtype: jax.typing.DTypeLike,
):
  return tpu.matmul_pop(
      ir.VectorType.get(
          ctx.lowering_context.dynamic_shape_replacement_fn(shape),
          _dtype_to_ir_type(dtype)),
      acc_addr,
      mxu_index,
  )

