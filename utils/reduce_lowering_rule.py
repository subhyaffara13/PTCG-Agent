
def reduce_lowering_rule(reduce_fn, type_to_kind, type_to_identity):
  def _lowering_rule(ctx: LoweringRuleContext, x, *, axes, **kwargs):
    (x_aval,) = ctx.avals_in
    if not ctx.avals_out[0].shape:
      # If reducing to a scalar, we reduce by adding a leading singleton
      # dimension and reducing over all other dimensions. This avoids
      # the materialization of a scalar tensor by the reduction op which
      # is not supported.
      def _proxy_fun(val, *, axes):
        val = val[jnp.newaxis, ...]
        axes = [axis + 1 for axis in axes]
        val = reduce_fn(val, axis=axes, keepdims=True)
        # Squeeze lowers to vector.ExtractOp which will place the final
        # value in a scalar register.
        return jnp.squeeze(val)
      proxy_lowering = lower_fun(_proxy_fun)
      return proxy_lowering(ctx, x, axes=axes)

    if jnp.issubdtype(x_aval.dtype, jnp.floating):
      kind = type_to_kind[jnp.floating]
      val = type_to_identity[jnp.floating]
      val = ir.FloatAttr.get(ctx.aval_to_ir_type(x_aval, shape=()), val)
    elif x_aval.dtype == jnp.int32:
      kind = type_to_kind[jnp.signedinteger]
      val = type_to_identity[jnp.signedinteger]
      val = ir.IntegerAttr.get(ir.IntegerType.get_signless(32), val)
    elif jnp.issubdtype(x_aval.dtype, jnp.unsignedinteger):
      raise NotImplementedError(
          "Reductions over unsigned integers not implemented."
      )
    else:
      raise NotImplementedError(
          f"Reductions over {x_aval.dtype} not implemented.")
    out_type = ctx.aval_to_ir_type(ctx.avals_out[0])
    identity = ir.DenseElementsAttr.get_splat(out_type, val)
    acc = arith.constant(out_type, identity)
    return vector.multi_reduction(kind, x, acc, axes)
  return _lowering_rule

