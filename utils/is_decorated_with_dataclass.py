
def is_decorated_with_dataclass(
    node: nodes.ClassDef, decorator_names: frozenset[str] = DATACLASSES_DECORATORS
) -> bool:
    """Return True if a decorated node has a `dataclass` decorator applied."""
    if not (isinstance(node, nodes.ClassDef) and node.decorators):
        return False

    return any(
        _looks_like_dataclass_decorator(decorator_attribute, decorator_names)
        for decorator_attribute in node.decorators.nodes
    )

