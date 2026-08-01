
def _resolve_schema_cls(cls):
    if isinstance(cls, str):
        resolved = getattr(schema, cls, None)
        if resolved is not None:
            return resolved
    if isinstance(cls, typing.ForwardRef):
        return _resolve_schema_cls(cls.__forward_arg__)
    return cls

