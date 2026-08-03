import itertools

def _lookup_in_mro(node, name) -> list:
    attrs = node.locals.get(name, [])

    nodes_ = itertools.chain.from_iterable(
        ancestor.locals.get(name, []) for ancestor in node.ancestors(recurs=True)
    )
    values = list(itertools.chain(attrs, nodes_))
    if not values:
        raise AttributeInferenceError(attribute=name, target=node)

    return values

