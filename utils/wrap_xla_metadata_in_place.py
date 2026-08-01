
def wrap_xla_metadata_in_place(ctx: LoweringRuleContext,
                               op: ir.Value | ir.Operation) -> None:
  if ctx.jaxpr_eqn_ctx is None:
    return
  if not ctx.jaxpr_eqn_ctx.xla_metadata:
    return
  op = _get_owner(op)
  if not isinstance(op, ir.Operation):
    return
  ctx_attributes = {}
  for k, v in ctx.jaxpr_eqn_ctx.xla_metadata.items():
    v_str = str(v).lower() if isinstance(v, bool) else str(v)
    ctx_attributes[k] = ir.StringAttr.get(v_str)
  _update_frontend_attributes(op, ctx_attributes)

