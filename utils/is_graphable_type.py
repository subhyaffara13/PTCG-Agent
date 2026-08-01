
def is_graphable_type(typ: type[object]) -> bool:
    """Return whether the given type is graphable."""
    return (
        issubclass(typ, torch.fx.node.base_types)
        or is_opaque_type(typ)
        or issubclass(typ, FakeScriptObject)
    )

