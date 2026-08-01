
def _get_device_type(device: str | torch.device) -> str:
    # Returns the device type as a string, e.g., "cpu" or "cuda"
    if isinstance(device, torch.device):
        device = str(device.type)
    if not isinstance(device, str):
        raise AssertionError(f"Expected device to be a str, got {type(device)}")
    return device.split(":")[0]


def _get_device_type(module: ir.Module) -> str | None:
  """Determines the device type based on the core_type annotations."""
  sparsecore_func_found = False
  tensorcore_func_found = False

  def assign_device_type_based_on_core_type(op: ir.Operation) -> ir.WalkResult:
    nonlocal sparsecore_func_found
    nonlocal tensorcore_func_found
    if op.name == "func.func":
      if "tpu.core_type" in op.attributes:
        core_type = op.attributes["tpu.core_type"]
        if str(core_type) in [
            f"#tpu.core_type<{c}>"
            for c in ["sc_scalar_subcore", "sc_vector_subcore"]
        ]:
          sparsecore_func_found = True
          if tensorcore_func_found:
            return ir.WalkResult.INTERRUPT
          return ir.WalkResult.SKIP
        if str(core_type) == "#tpu.core_type<tc>":
          tensorcore_func_found = True
          return ir.WalkResult.SKIP
        raise ValueError(f"Unknown core type: {core_type}")
    return ir.WalkResult.ADVANCE

  module.operation.walk(
      assign_device_type_based_on_core_type, walk_order=ir.WalkOrder.PRE_ORDER
  )
  if tensorcore_func_found and sparsecore_func_found:
    raise ValueError(
        "A single Mosaic kernel cannot contain both TensorCore and SparseCore"
        " functions."
    )
  if sparsecore_func_found:
    return "sparsecore"
  return None

