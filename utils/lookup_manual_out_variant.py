
def lookup_manual_out_variant(
    op: torch._ops.OpOverload,
) -> torch._ops.OpOverload | None:
    """Return the manually registered out variant for op, or None."""
    return _manual_out_variant_registry.get(op)

