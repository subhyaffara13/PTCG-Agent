
def dataclass_tag_callback(ctx: ClassDefContext) -> None:
    """Record that we have a dataclass in the main semantic analysis pass.

    The later pass implemented by DataclassTransformer will use this
    to detect dataclasses in base classes.
    """
    add_dataclass_tag(ctx.cls.info)

