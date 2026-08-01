
def attr_tag_callback(ctx: mypy.plugin.ClassDefContext) -> None:
    """Record that we have an attrs class in the main semantic analysis pass.

    The later pass implemented by attr_class_maker_callback will use this
    to detect attrs classes in base classes.
    """
    # The value is ignored, only the existence matters.
    ctx.cls.info.metadata["attrs_tag"] = {}

