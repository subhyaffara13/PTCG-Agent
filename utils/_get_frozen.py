
def _get_frozen(ctx: mypy.plugin.ClassDefContext, frozen_default: bool) -> bool:
    """Return whether this class is frozen."""
    if _get_decorator_bool_argument(ctx, "frozen", frozen_default):
        return True
    # Subclasses of frozen classes are frozen so check that.
    for super_info in ctx.cls.info.mro[1:-1]:
        if "attrs" in super_info.metadata and super_info.metadata["attrs"]["frozen"]:
            return True
    return False

