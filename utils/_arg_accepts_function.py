
def _arg_accepts_function(typ: ProperType) -> bool:
    return (
        # TypeVar / Callable
        isinstance(typ, (TypeVarType, CallableType))
        or
        # Protocol with __call__
        isinstance(typ, Instance)
        and typ.type.is_protocol
        and typ.type.get_method("__call__") is not None
    )

