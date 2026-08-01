
def _use_cutlass_for_op(op_name: str) -> bool:
    """Check if CUTLASS should be used for the given operation."""
    enabled_ops = config.cutlass.cutlass_enabled_ops.upper()
    if enabled_ops == "ALL":
        return True
    return op_name.upper() in [x.strip() for x in enabled_ops.split(",")]

