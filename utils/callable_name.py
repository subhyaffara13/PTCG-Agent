
def callable_name(type: FunctionLike) -> str | None:
    name = type.get_name()
    if name is not None and name[0] != "<":
        return f'"{name}"'.replace(" of ", '" of "')
    return name

