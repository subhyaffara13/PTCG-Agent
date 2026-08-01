
def _remove_hashability(ctx: mypy.plugin.ClassDefContext) -> None:
    """Remove hashability from a class."""
    add_attribute_to_class(
        ctx.api, ctx.cls, "__hash__", NoneType(), is_classvar=True, overwrite_existing=True
    )

