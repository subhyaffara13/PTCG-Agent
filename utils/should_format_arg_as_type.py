
def should_format_arg_as_type(arg_kind: ArgKind, arg_name: str | None, verbosity: int) -> bool:
    """
    Determine whether a function argument should be formatted as its Type or with name.
    """
    return (arg_kind == ARG_POS and arg_name is None) or (
        verbosity == 0 and arg_kind.is_positional()
    )

