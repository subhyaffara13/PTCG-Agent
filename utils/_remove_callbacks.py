
def _remove_callbacks(m: ir.Module, ignore_callbacks: IgnoreCallbacks):
  """Removes callback pointers from precompiled IR.

  Python function pointers are not deterministic across executions.
  """
  def _update_bc_attribute(op: ir.Operation) -> ir.WalkResult:
    if "call_target_name" not in op.attributes:
      return ir.WalkResult.ADVANCE
    call_target_name = op.attributes["call_target_name"]
    assert isinstance(call_target_name, ir.StringAttr)
    if op.name == "stablehlo.custom_call" and (
        (
            ignore_callbacks == IgnoreCallbacks.ALL
            and call_target_name.value.endswith("callback")
        )
        or call_target_name.value == "CustomSPMDPartitioning"
    ):
      op.attributes["backend_config"] = ir.StringAttr.get("REMOVED")
    return ir.WalkResult.ADVANCE

  if ignore_callbacks == IgnoreCallbacks.NO:
    return m

  m.operation.walk(_update_bc_attribute)
  return m

