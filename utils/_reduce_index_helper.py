
def _reduce_index_helper(
    ctx: LoweringRuleContext, x, axes, index_dtype, reduction_kind):
  (x_aval,) = ctx.avals_in
  (out_aval,) = ctx.avals_out
  if x_aval.dtype != jnp.float32:
    raise NotImplementedError("Only float32 is supported")
  if len(axes) != 1:
    raise NotImplementedError("Only single axis reduction supported")
  if index_dtype != jnp.int32:
    raise NotImplementedError("Only index_dtype=int32 is supported")

  axis = axes[0]
  # TODO(b/460843515): Support 1D inputs in Mosaic.
  is_1d = len(x_aval.shape) == 1
  if is_1d:
    x_2d_aval = jax_core.ShapedArray((1, *x_aval.shape), x_aval.dtype)
    x_2d_type = ctx.aval_to_ir_type(x_2d_aval)
    out_aval = jax_core.ShapedArray((1, *out_aval.shape), out_aval.dtype)
    x = vector.shape_cast(x_2d_type, x)
    axis += 1

  out_type = ctx.aval_to_ir_type(out_aval)
  result = tpu.reduce_index(out_type, x, axis, reduction_kind)
  if is_1d:
    return vector.extract(result, [], [0])
  return result

