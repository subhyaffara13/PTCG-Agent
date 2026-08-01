
def register_function(
    ctx: PluginContext,
    singledispatch_obj: Instance,
    func: Type,
    options: Options,
    register_arg: Type | None = None,
) -> None:
    """Register a function"""

    func = get_proper_type(func)
    if not isinstance(func, CallableType):
        return
    metadata = get_singledispatch_info(singledispatch_obj)
    if metadata is None:
        # if we never added the fallback to the type variables, we already reported an error, so
        # just don't do anything here
        return
    dispatch_type = get_dispatch_type(func, register_arg)
    if dispatch_type is None:
        # TODO: report an error here that singledispatch requires at least one argument
        # (might want to do the error reporting in get_dispatch_type)
        return
    fallback = metadata.fallback

    fallback_dispatch_type = fallback.arg_types[0]
    if not is_subtype(dispatch_type, fallback_dispatch_type):
        fail(
            ctx,
            "Dispatch type {} must be subtype of fallback function first argument {}".format(
                format_type(dispatch_type, options), format_type(fallback_dispatch_type, options)
            ),
            func.definition,
        )
        return
    return

