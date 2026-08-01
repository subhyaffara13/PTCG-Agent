
def from_attributes_callback(ctx: MethodContext) -> Type:
    """Raise an error if from_attributes is not enabled."""
    model_type: Instance
    ctx_type = ctx.type
    if isinstance(ctx_type, TypeType):
        ctx_type = ctx_type.item
    if isinstance(ctx_type, CallableType) and isinstance(ctx_type.ret_type, Instance):
        model_type = ctx_type.ret_type  # called on the class
    elif isinstance(ctx_type, Instance):
        model_type = ctx_type  # called on an instance (unusual, but still valid)
    else:  # pragma: no cover
        detail = f'ctx.type: {ctx_type} (of type {ctx_type.__class__.__name__})'
        error_unexpected_behavior(detail, ctx.api, ctx.context)
        return ctx.default_return_type
    pydantic_metadata = model_type.type.metadata.get(METADATA_KEY)
    if pydantic_metadata is None:
        return ctx.default_return_type
    if not model_type.type.has_base(BASEMODEL_FULLNAME):
        # not a Pydantic v2 model
        return ctx.default_return_type
    from_attributes = pydantic_metadata.get('config', {}).get('from_attributes')
    if from_attributes is not True:
        error_from_attributes(model_type.type.name, ctx.api, ctx.context)
    return ctx.default_return_type

