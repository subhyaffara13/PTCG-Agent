
def unwrap_simple_optional_type(optional_type: type) -> type:
    """Unwraps a simple optional type, i.e. returns Type from Optional[Type]."""
    for arg in get_args(optional_type):
        if arg is not type(None):
            return arg
    raise ValueError(f"'{optional_type}' is not an optional type")

