
def register_out_variant(
    functional_op: torch._ops.OpOverload,
    out_op: torch._ops.OpOverload,
) -> None:
    """Register a functional op -> out variant mapping."""
    _manual_out_variant_registry[functional_op] = out_op

