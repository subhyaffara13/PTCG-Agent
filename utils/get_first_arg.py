
def get_first_arg(tp: CallableType) -> str | None:
    definition = get_func_def(tp)
    if not isinstance(definition, FuncDef) or not definition.info or definition.is_static:
        return None
    return definition.original_first_arg


def get_first_arg(args: list[list[T]]) -> T | None:
    """Get the element that corresponds to the first argument passed to the function"""
    if args and args[0]:
        return args[0][0]
    return None

