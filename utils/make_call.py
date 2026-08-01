
def make_call(*items: tuple[str, str | None]) -> CallExpr:
    args: list[Expression] = []
    arg_names = []
    arg_kinds = []
    for arg, name in items:
        shortname = arg.split(".")[-1]
        n = NameExpr(shortname)
        n.fullname = arg
        args.append(n)
        arg_names.append(name)
        if name:
            arg_kinds.append(ARG_NAMED)
        else:
            arg_kinds.append(ARG_POS)
    return CallExpr(NameExpr("f"), args, arg_kinds, arg_names)

