
def io_callback_lowering(ctx, *args, callback, sharding, ordered, **params):
  def _callback(*flat_args):
    return tuple(
        io_callback_impl(
            *flat_args,
            callback=callback,
            sharding=None,  # unused.
            ordered=ordered,
            **params,
        )
    )

  op_sharding = _callback_op_sharding(
      ctx.module_context.axis_context, sharding, ctx.avals_out)
  if ordered:
    token = ctx.tokens_in.get(_OrderedIOEffect)
    result, token, _ = emit_python_callback(
        ctx,
        _callback,
        token,
        list(args),
        ctx.avals_in,
        ctx.avals_out,
        has_side_effect=True,
        returns_token=True,
        sharding=op_sharding,
    )
    ctx.set_tokens_out(
        ctx.tokens_in.update_tokens(mlir.TokenSet({_OrderedIOEffect: token})))
  else:
    result, _, _ = emit_python_callback(
        ctx,
        _callback,
        None,
        list(args),
        ctx.avals_in,
        ctx.avals_out,
        has_side_effect=True,
        returns_token=False,
        sharding=op_sharding,
    )
  return result

