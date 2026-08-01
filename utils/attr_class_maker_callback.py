
def attr_class_maker_callback(
    ctx: mypy.plugin.ClassDefContext,
    auto_attribs_default: bool | None = False,
    frozen_default: bool = False,
    slots_default: bool = False,
) -> bool:
    """Add necessary dunder methods to classes decorated with attr.s.

    attrs is a package that lets you define classes without writing dull boilerplate code.

    At a quick glance, the decorator searches the class body for assignments of `attr.ib`s (or
    annotated variables if auto_attribs=True), then depending on how the decorator is called,
    it will add an __init__ or all the compare methods.
    For frozen=True it will turn the attrs into properties.

    Hashability will be set according to https://www.attrs.org/en/stable/hashing.html.

    See https://www.attrs.org/en/stable/how-does-it-work.html for information on how attrs works.

    If this returns False, some required metadata was not ready yet, and we need another
    pass.
    """
    with state.strict_optional_set(ctx.api.options.strict_optional):
        # This hook is called during semantic analysis, but it uses a bunch of
        # type-checking ops, so it needs the strict optional set properly.
        return attr_class_maker_callback_impl(
            ctx, auto_attribs_default, frozen_default, slots_default
        )

