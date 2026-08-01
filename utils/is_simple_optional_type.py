
def is_simple_optional_type(type_: type) -> bool:
    """Check if a type is optional, i.e. Optional[Type] or Union[Type, None] or Type | None, where Type is a non-composite type."""
    if get_origin(type_) in UNION_TYPES:
        union_args = get_args(type_)
        if len(union_args) == 2 and type(None) in union_args:
            return True
    return False

