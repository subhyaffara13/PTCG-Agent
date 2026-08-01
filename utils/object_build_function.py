
def object_build_function(
    node: nodes.Module | nodes.ClassDef, member: _FunctionTypes
) -> nodes.FunctionDef:
    """create astroid for a living function object"""
    (
        args,
        posonlyargs,
        defaults,
        kwonlyargs,
        kwonly_defaults,
    ) = _get_args_info_from_callable(member)

    return build_function(
        getattr(member, "__name__", "<no-name>"),
        node,
        args,
        posonlyargs,
        defaults,
        member.__doc__ if isinstance(member.__doc__, str) else None,
        kwonlyargs=kwonlyargs,
        kwonlydefaults=kwonly_defaults,
    )

