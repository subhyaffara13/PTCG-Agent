
def extract_dunder_match_args_names(info: TypeInfo) -> list[str]:
    ty = info.names.get("__match_args__")
    assert ty
    match_args_type = get_proper_type(ty.type)
    assert isinstance(match_args_type, TupleType), match_args_type

    match_args: list[str] = []
    for item in match_args_type.items:
        proper_item = get_proper_type(item)

        match_arg = None
        if isinstance(proper_item, Instance) and proper_item.last_known_value:
            match_arg = proper_item.last_known_value.value
        elif isinstance(proper_item, LiteralType):
            match_arg = proper_item.value
        assert isinstance(match_arg, str), f"Unrecognized __match_args__ item: {item}"

        match_args.append(match_arg)
    return match_args

