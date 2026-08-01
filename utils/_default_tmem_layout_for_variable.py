
def _default_tmem_layout_for_variable(
    variable: cs.Variable,
) -> tcgen05.TMEMLayout | None:
  """Returns a default TMEM layout for the given variable, if one is defined."""
  value = variable.key.value
  parent = value.owner
  if isinstance(parent, mgpu.TmemAllocOp):
    return tcgen05._infer_tmem_layout(
        tuple(value.type.shape), bool(parent.collective), packing=1
    )
  return None

