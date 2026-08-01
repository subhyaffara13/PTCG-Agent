
def attributes(func: FunctionSchema, owning: bool = True) -> list[Binding]:
    args = func.arguments.flat_all
    if args[0].type != BaseType(BaseTy.Tensor):
        raise AssertionError(f"Expected first arg to be Tensor, got {args[0].type}")
    return [
        reapply_views_binding,
        inverse_return_mode_binding,
        *[dispatcher.argument(a, remove_non_owning_ref_types=owning) for a in args[1:]],
    ]


def attributes(obj):
    disallowed_names = {name for name, value in getmembers(type(obj)) if isinstance(value, FunctionType)}
    return {
        name: getattr(obj, name)
        for name in dir(obj)
        if name[0] != "_" and name not in disallowed_names and hasattr(obj, name)
    }

