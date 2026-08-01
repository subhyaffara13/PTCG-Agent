
def _add_slots(ctx: mypy.plugin.ClassDefContext, attributes: list[Attribute]) -> None:
    if any(p.slots is None for p in ctx.cls.info.mro[1:-1]):
        # At least one type in mro (excluding `self` and `object`)
        # does not have concrete `__slots__` defined. Ignoring.
        return

    # Unlike `@dataclasses.dataclass`, `__slots__` is rewritten here.
    ctx.cls.info.slots = {attr.name for attr in attributes}

    # Also, inject `__slots__` attribute to class namespace:
    slots_type = TupleType(
        [ctx.api.named_type("builtins.str") for _ in attributes],
        fallback=ctx.api.named_type("builtins.tuple"),
    )
    add_attribute_to_class(api=ctx.api, cls=ctx.cls, name="__slots__", typ=slots_type)

