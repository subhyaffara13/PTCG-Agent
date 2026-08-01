
def get_all_elements(
    node: nodes.NodeNG,
) -> Iterable[nodes.NodeNG]:
    """Recursively returns all atoms in nested lists and tuples."""
    if isinstance(node, (nodes.Tuple, nodes.List)):
        for child in node.elts:
            yield from get_all_elements(child)
    else:
        yield node

