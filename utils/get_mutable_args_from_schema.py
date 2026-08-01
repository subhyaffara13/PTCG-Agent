
def get_mutable_args_from_schema(
    schema: torch.FunctionSchema,
) -> tuple[list[str], list[torch.Type]]:
    """
    Returns the list of argument names that get mutated according to the
    schema and their types.
    """
    mutable_args_names = [
        arg.name
        for arg in schema.arguments
        if arg.alias_info is not None and arg.alias_info.is_write
    ]

    mutable_args_types = [
        arg.type
        for arg in schema.arguments
        if arg.alias_info is not None and arg.alias_info.is_write
    ]
    return mutable_args_names, mutable_args_types  # type: ignore[return-value]

