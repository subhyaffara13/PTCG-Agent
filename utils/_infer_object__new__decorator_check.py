
def _infer_object__new__decorator_check(node) -> bool:
    """Predicate before inference_tip.

    Check if the given ClassDef has an @object.__new__ decorator
    """
    if not node.decorators:
        return False

    for decorator in node.decorators.nodes:
        if isinstance(decorator, nodes.Attribute):
            if decorator.as_string() == OBJECT_DUNDER_NEW:
                return True
    return False

