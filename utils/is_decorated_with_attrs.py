
def is_decorated_with_attrs(node, decorator_names=ATTRS_NAMES) -> bool:
    """Return whether a decorated node has an attr decorator applied."""
    if not node.decorators:
        return False
    for decorator_attribute in node.decorators.nodes:
        if isinstance(decorator_attribute, nodes.Call):  # decorator with arguments
            decorator_attribute = decorator_attribute.func
        if decorator_attribute.as_string() in decorator_names:
            return True

        inferred = safe_infer(decorator_attribute)
        if inferred and inferred.root().name == "attr._next_gen":
            return True
    return False

