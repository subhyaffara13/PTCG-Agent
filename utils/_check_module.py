
def _check_module(mod: ir.Module, *,
                  disabled_checks: Sequence[DisabledSafetyCheck],
                  shardy_enabled: bool) -> bool:
  """Run a number of checks on the module.

  Args:
    disabled_checks: the safety checks that are disabled.

  Returns True if the module uses non-replicated shardings.
  """
  sharding_attr = ir.StringAttr.get("Sharding", mod.context)
  allowed_custom_call_targets: set[str] = copy.copy(_CUSTOM_CALL_TARGETS_GUARANTEED_STABLE)
  for dc in disabled_checks:
    target = dc.is_custom_call()
    if target is not None:
      allowed_custom_call_targets.add(target)

  allowed_custom_call_targets_attrs = {
      ir.StringAttr.get(target, mod.context)
      for target in allowed_custom_call_targets}
  disallowed_custom_call_ops: list[str] = []
  module_uses_non_replicated_sharding = False

  has_non_replicated_sharding = (
      _has_non_replicated_sharding_sdy if shardy_enabled else
      _has_non_replicated_sharding_mhlo
  )

  all_custom_calls_allowed = "ALL" in allowed_custom_call_targets

  def check_op(op: ir.Operation):
    nonlocal module_uses_non_replicated_sharding
    op_name = op.operation.name
    if op_name == "func.func":
      if has_non_replicated_sharding(op.operation):
        module_uses_non_replicated_sharding = True

    elif op_name == "stablehlo.custom_call":
      call_target_name_attr = op.operation.attributes["call_target_name"]
      if (
          not all_custom_calls_allowed
          and call_target_name_attr not in allowed_custom_call_targets_attrs
      ):
        disallowed_custom_call_ops.append(f"{op} at {op.location}")
      if call_target_name_attr == sharding_attr:
        if has_non_replicated_sharding(op):
          module_uses_non_replicated_sharding = True
    elif op_name == "sdy.sharding_constraint":
      if has_non_replicated_sharding(op):
        module_uses_non_replicated_sharding = True

  def walk_operations(op: ir.Operation) -> None:
    check_op(op)
    for region in op.operation.regions:
      for block in region:
        for block_op in block:
          walk_operations(block_op.operation)

  walk_operations(mod.operation)
  if disallowed_custom_call_ops:
    disallowed_custom_call_ops_str = "\n".join(disallowed_custom_call_ops)
    msg = ("Cannot serialize code with custom calls whose targets have no "
           "compatibility guarantees. "
           "See https://docs.jax.dev/en/latest/export/export.html#compatibility-guarantees-for-custom-calls. "
           "Examples are:\n"
           f"{disallowed_custom_call_ops_str}.\n")
    raise ValueError(msg)
  return module_uses_non_replicated_sharding

