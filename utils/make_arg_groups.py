
def make_arg_groups(args: list[RuntimeArg]) -> dict[ArgKind, list[RuntimeArg]]:
    """Group arguments by kind."""
    return {k: [arg for arg in args if arg.kind == k] for k in ArgKind}

