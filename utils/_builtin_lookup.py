
def _builtin_lookup(node, name) -> list:
    values = node.locals.get(name, [])
    if not values:
        raise AttributeInferenceError(attribute=name, target=node)

    return values

