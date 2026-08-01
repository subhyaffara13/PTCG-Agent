
def call_singledispatch_function_callback(ctx: MethodSigContext) -> FunctionLike:
    """Called for functools._SingleDispatchCallable.__call__"""
    if not isinstance(ctx.type, Instance):
        return ctx.default_signature
    metadata = get_singledispatch_info(ctx.type)
    if metadata is None:
        return ctx.default_signature
    return metadata.fallback

