
def get_registered_op_names() -> list[str]:
    """Get all op names that have DTensor sharding rules and also have OpInfo.

    Returns OpInfo names (which may differ from aten base names, e.g.,
    "nn.functional.relu" instead of "relu").
    """

    propagator = DTensor._op_dispatcher.sharding_propagator

    # Get all registered aten ops
    all_registered = set(propagator.op_single_dim_strategy_funcs.keys()) | set(
        propagator.op_strategy_funcs.keys()
    )

    # Extract base names (aten.mul.Tensor -> mul)
    base_names = set()
    for op in all_registered:
        parts = str(op).split(".")
        if len(parts) >= 2:
            base_names.add(parts[1])

    # Build mappings from OpInfo: both by name and by aten_name
    opinfo_by_name = {}
    opinfo_by_aten_name: dict[str, list[str]] = {}
    for op in op_db:
        opinfo_by_name[op.name] = True
        opinfo_by_aten_name.setdefault(op.aten_name, []).append(op.name)

    result = set()
    for base_name in base_names:
        if base_name in opinfo_by_name:
            # Direct match (e.g., "add" -> OpInfo named "add")
            result.add(base_name)
        elif base_name in opinfo_by_aten_name:
            # Match via aten_name (e.g., "relu" -> OpInfo "nn.functional.relu"
            # which has aten_name="relu")
            result.update(opinfo_by_aten_name[base_name])

    return sorted(result)

