
def _has_abstract_methods(node: nodes.ClassDef) -> bool:
    """Determine if the given `node` has abstract methods.

    The methods should be made abstract by decorating them
    with `abc` decorators.
    """
    return len(utils.unimplemented_abstract_methods(node)) > 0

