
def num_positional_args(arg_values: list[Value], arg_kinds: list[ArgKind] | None) -> int:
    if arg_kinds is None:
        return len(arg_values)
    num_pos = 0
    for kind in arg_kinds:
        if kind == ARG_POS:
            num_pos += 1
    return num_pos

