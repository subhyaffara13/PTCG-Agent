import functools

def check_lowering_rule(ctx, *args, err_tree, debug):
  if debug:
    # NOOP (check will only trigger when discharged)
    return []
  if not config.xla_runtime_errors.value:
    raise functionalization_error

  out_op, _, _ = callback.emit_python_callback(
      ctx, callback=functools.partial(python_err, err_tree),
      token=None,
      operands=args,
      operand_avals=list(ctx.avals_in),
      result_avals=list(ctx.avals_out),
      has_side_effect=True,
      returns_token=False)
  return out_op

