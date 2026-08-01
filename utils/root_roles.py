
def root_roles() -> list[SpanRole]:
    """Roles that start a new trace (no in-process parent)."""
    return [role for role, spec in SPAN_REGISTRY.items() if spec.parent is None]

