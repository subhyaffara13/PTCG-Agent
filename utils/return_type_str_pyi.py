
def return_type_str_pyi(t: Type) -> str:
    # Where arguments are open to accepting Union, return types should return
    # concrete types

    if isinstance(t, OptionalType):
        inner = return_type_str_pyi(t.elem)
        return f"{inner} | None".replace(" | None | None", " | None")

    if isinstance(t, BaseType):
        if t.name == BaseTy.Device:
            return "_device"
        elif t.name == BaseTy.Dimname:
            return "str | None"
        else:
            return argument_type_str_pyi(t)

    if isinstance(t, ListType):
        inner = return_type_str_pyi(t.elem)
        return f"tuple[{inner}, ...]"

    return argument_type_str_pyi(t)

