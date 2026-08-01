
def _check_lowering_rule(
    ctx: LoweringRuleContext, *err_args, err_tree, debug
):
  del ctx  # Unused.

  if not debug:
    raise NotImplementedError(
        "Non-debug checks are not supported by the Mosaic backend."
        " Functionalize them via `jax.experimental.checkify`."
    )
  if not pallas_core.debug_checks_enabled():
    return []

  error = jax.tree.unflatten(err_tree, err_args)
  [pred] = error._pred.values()
  [exception_tree] = error._metadata.values()
  [payload] = error._payload.values()
  exception = jax.tree.unflatten(exception_tree, payload)
  assert isinstance(exception, checkify.FailedCheckError)
  assert isinstance(exception, checkify.FailedCheckError)

  # check_p has an inverted predicate compared to assert, so we need to compute
  # ``not pred`` here.
  minus_one = ir_constant(-1, _dtype_to_ir_type(jnp.bool))
  not_pred = arith.xori(pred, minus_one)
  cf.assert_(not_pred, exception.fmt_string)
  return []


def _check_lowering_rule(ctx: LoweringRuleContext, *err_args, err_tree, debug):
  if not debug:
    raise NotImplementedError(
        "Non-debug checks are not supported by the Mosaic GPU backend."
        " Functionalize them via `jax.experimental.checkify`."
    )
  if not pallas_core.debug_checks_enabled():
    return []

  error = jax.tree.unflatten(err_tree, err_args)
  [pred] = error._pred.values()
  [exception_tree] = error._metadata.values()
  [payload] = error._payload.values()
  exception = jax.tree.unflatten(exception_tree, payload)
  assert isinstance(exception, checkify.FailedCheckError)

  # check_p has an inverted predicate compared to assert, so we need to compute
  # ``not pred`` here.
  minus_one = _ir_constant(-1, mgpu_utils.dtype_to_ir_type(jnp.bool))
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    pred = pred.registers.item()
  not_pred = arith_dialect.xori(pred, minus_one)
  cf_dialect.assert_(not_pred, exception.fmt_string)
  return []

