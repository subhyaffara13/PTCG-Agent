
def has_starred_node_recursive(
    node: nodes.For | nodes.Comprehension | nodes.Set | nodes.Starred,
) -> Iterator[bool]:
    """Yield ``True`` if a Starred node is found recursively."""
    match node:
        case nodes.Starred():
            yield True
        case nodes.Set():
            for elt in node.elts:
                yield from has_starred_node_recursive(elt)
        case nodes.For() | nodes.Comprehension():
            for elt in node.iter.elts:
                yield from has_starred_node_recursive(elt)

