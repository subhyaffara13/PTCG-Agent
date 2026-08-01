
def foreach_map_fn(*args: Any) -> Any:
    op = args[0]
    new_args: list[Any] = []
    at_least_one_list = False
    for arg in args[1:]:
        if not isinstance(arg, (list, tuple)):
            new_args.append(_repeat(arg))
        else:
            at_least_one_list = True
            new_args.append(arg)

    # Just apply op once to args if there are no lists
    if not at_least_one_list:
        return op(*args[1:])

    out = []
    for unpacked in zip(*new_args):
        out.append(op(*unpacked))

    return out

