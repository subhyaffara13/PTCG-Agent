
def _resolve_pydantic_type(typ) -> List:
    """Resolve the actual TypedDict class from a potentially wrapped type."""
    origin = get_origin(typ)
    typs = []
    if origin is Union:  # Check if it's a Union (like Optional)
        for arg in get_args(typ):
            if (
                arg is not None
                and not isinstance(arg, type(None))
                and "NoneType" not in str(arg)
            ):
                typs.append(arg)
    elif isinstance(typ, type) and isinstance(typ, BaseModel):
        return [typ]
    return typs

