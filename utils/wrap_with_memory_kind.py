
def wrap_with_memory_kind(
    ctx: ModuleContext, x: ir.Value, memory_kind: str, aval_out: core.AbstractValue) -> ir.Value:
  if aval_out is None:
    result_type = x.type
  else:
    (result_type,) = aval_to_ir_types(ctx, aval_out)
  op = custom_call("annotate_device_placement", result_types=[result_type],
                   operands=[x], has_side_effect=True, api_version=1)
  op.attributes["mhlo.frontend_attributes"] = ir.DictAttr.get({
      "_xla_buffer_placement": ir.StringAttr.get(memory_kind)
  })
  return op.result

