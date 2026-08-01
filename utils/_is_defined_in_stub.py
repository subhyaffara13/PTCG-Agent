
def _is_defined_in_stub(ctx: mypy.plugin.AttributeContext) -> bool:
    assert isinstance(ctx.api, TypeCheckerSharedApi)
    return isinstance(ctx.type, Instance) and ctx.api.is_defined_in_stub(ctx.type)

