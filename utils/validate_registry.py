
def validate_registry(
    registry: dict[SpanRole, SpanSpec] | None = None,
) -> None:
    reg = registry if registry is not None else SPAN_REGISTRY
    for role, spec in reg.items():
        if spec.role is not role:
            raise ValueError(f"SPAN_REGISTRY[{role}] has mismatched role {spec.role}")
        if spec.parent is not None and spec.parent not in reg:
            raise ValueError(f"span role {role} declares unknown parent {spec.parent}")
    missing = [role for role in SpanRole if role not in reg]
    if missing:
        raise ValueError(f"SPAN_REGISTRY is missing roles: {missing}")

