
def dataclass_class_maker_callback(ctx: ClassDefContext) -> bool:
    """Hooks into the class typechecking process to add support for dataclasses."""
    if any(i.is_named_tuple for i in ctx.cls.info.mro):
        ctx.api.fail("A NamedTuple cannot be a dataclass", ctx=ctx.cls.info)
        return True
    transformer = DataclassTransformer(
        ctx.cls, ctx.reason, _get_transform_spec(ctx.reason), ctx.api
    )
    return transformer.transform()

