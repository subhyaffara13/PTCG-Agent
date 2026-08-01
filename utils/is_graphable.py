
def is_graphable(val: object) -> TypeIs[torch.fx.node.BaseArgumentTypes]:
    """Definition: a graphable type is a type that is an acceptable input/output type to a FX node."""
    return isinstance(
        val, (*torch.fx.node.base_types, FakeScriptObject)
    ) or is_opaque_type(type(val))

