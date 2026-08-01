
def _apply_modify_schema(
    modify_schema: Callable[..., None], field: Optional[ModelField], field_schema: Dict[str, Any]
) -> None:
    from inspect import signature

    sig = signature(modify_schema)
    args = set(sig.parameters.keys())
    if 'field' in args or 'kwargs' in args:
        modify_schema(field_schema, field=field)
    else:
        modify_schema(field_schema)

