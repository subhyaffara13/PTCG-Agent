
def is_forward_derivative_definition(
    all_arg_names: list[str], names: tuple[str, ...]
) -> bool:
    for name in names:
        return name not in all_arg_names
    raise RuntimeError("Expected `names` to be non-empty")

