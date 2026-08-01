
def _xla_metadata_value_lowering_rule(
    ctx: mlir.LoweringRuleContext, val: ir.Value, *, xla_metadata_kvs
):
  xla_metadata = dict(xla_metadata_kvs)
  op_to_attach_metadata = _target_op_to_attach_metadata(val)
  if op_to_attach_metadata is not None:
    _attach_xla_metadata_to_op(xla_metadata, op_to_attach_metadata)
  return [val]

