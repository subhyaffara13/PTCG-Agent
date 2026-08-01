
def child_roles(parent: SpanRole) -> list[SpanRole]:
    return [role for role, spec in SPAN_REGISTRY.items() if spec.parent == parent]

