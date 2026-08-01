
def wrap_compute_type_in_place(ctx: LoweringRuleContext,
                               op: ir.Value | ir.Operation) -> None:
  if ctx.jaxpr_eqn_ctx is None or ctx.jaxpr_eqn_ctx.compute_type is None:
    return
  op = _get_owner(op)

  if ctx.jaxpr_eqn_ctx.compute_type.startswith("gpu_stream:"):
    _, stream = ctx.jaxpr_eqn_ctx.compute_type.split(":", 1)
    dict_attr = {
        "_xla_stream_annotation": ir.StringAttr.get(stream),
        "inlineable": ir.StringAttr.get("false")
    }
  else:
    dict_attr = {
        "_xla_compute_type": ir.StringAttr.get(
            map_compute_type(ctx.jaxpr_eqn_ctx.compute_type))
    }
  _update_frontend_attributes(op, dict_attr)

