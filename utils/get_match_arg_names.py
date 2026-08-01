
def get_match_arg_names(typ: TupleType) -> list[str | None]:
    args: list[str | None] = []
    for item in typ.items:
        values = try_getting_str_literals_from_type(item)
        if values is None or len(values) != 1:
            args.append(None)
        else:
            args.append(values[0])
    return args

